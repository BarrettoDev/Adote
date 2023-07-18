from django.shortcuts import render, redirect
from divulgar.models import Pet
from django.contrib.messages import constants
from django.contrib import messages
from .models import PedidoAdocao
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


def listar_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(status="P")

        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')

        if cidade:
            pets = pets.filter(cidade__icontains=cidade)
        
        if raca_filter:
            raca__id=raca_filter

        return render(request, 'listar_pets.html', {'pets': pets})

@login_required
def pedido_adocao(request, id_pet):
    pet = Pet.objects.filter(id=id_pet).filter(status="P")

    if not pet.exists():
        messages.add_message(request, constants.WARNING, 'Esse pet já foi adotado')
        return redirect('/adotar')
    
    pedido = PedidoAdocao(pet=pet.first(),
                        usuario=request.user,
                        data=datetime.now())
    
    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido realizado')

    return redirect('/adotar')

@login_required
def processa_pedido_adocao(request, id_pedido, pet_id):
    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id=id_pedido)
    pet = Pet.objects.get(id=pet_id)

    if status == 'A':
        pedido.status = 'AP'
        string = '''Olá, sua solicitação de adoção foi aprovada'''
        messages.add_message(request, constants.SUCCESS, 'Pedido aprovado')
        pet.status = 'A'
    elif status == 'R':
        pedido.status = 'R'
        string = '''Olá, sua solicitação de adoção foi recusada'''
        messages.add_message(request, constants.ERROR, 'Pedido recusado')

    pedido.save()
    pet.save()

    print(pedido.usuario.email)
    email = send_mail(
        'Pedido de Adoção',
        string,
        'denilson7lb@gmail.com',
        [pedido.usuario.email,]
    )

    return redirect('/divulgar/ver_pedido_adocao')
