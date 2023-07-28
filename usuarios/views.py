from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# Create your views here.
def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')
    if request.method == "GET":
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0 or len(confirmar_senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return render(request, 'cadastro.html')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senha diferentes digitadas')
            return render(request, 'cadastro.html')

        try:
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )
            # Mensagem de sucesso
            messages.add_message(request, constants.SUCCESS, 'Usuario criado com exito') 
            return render(request, 'cadastro.html')
        except:
            # Mensagem de Erro
            messages.add_message(request, constants.ERROR, 'Erro no sistema')
            return render(request, 'cadastro.html')

def logar(request):
    if request.user.is_authenticated:
        return redirect('/divulgar/novo_pet')
    
    elif request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')

        user = authenticate(username=nome,
                            password=senha)

        if user is not None:
            login(request, user)
            return redirect('/divulgar/novo_pet')

        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos')
            return render(request, 'login.html')

def sair(request):
    logout(request)
    return redirect('/auth/login')

def my_view(request):
    # Carrega o conteúdo do primeiro arquivo JSON
    with open("usuarios\templates\logo2.json") as json_file:
        gif1 = json.load(json_file)
    
    # Carrega o conteúdo do segundo arquivo JSON
    with open("usuarios\templates\img2.json") as json_file:
        gif2 = json.load(json_file)
    
    # Passa o conteúdo dos arquivos JSON para o template
    return render(request, 'my_template.html', {'gif1': gif1, 'gif2': gif2})
