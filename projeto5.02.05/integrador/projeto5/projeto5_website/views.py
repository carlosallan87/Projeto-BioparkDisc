from email import message
import operator
from turtle import title
from django.shortcuts import render
from projeto5_website.models import Pergunta, Alternativa, Aluno, CHOICES_ALTERNATIVA, Resultado, Link, Instituicao
from django.http import HttpResponse, HttpResponseRedirect
from projeto5_website.forms import PerguntaForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import pytz

# Create your views here.
utc=pytz.UTC

def home(request):
  return render(request, "projeto5_website/teste/1.html", 
        {"perguntas": Pergunta.objects.all()})

def pergunta_form(request):
  if request.method == "POST":
    form = PerguntaForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/') #Lembrar de importar
  else:
    form = PerguntaForm()
  return render(request, "projeto5_website/pergunta_form.html", {'form': form})

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/resultado/')
                
    return render(request, 'projeto5_website/login.html')


def teste(request, id):
  #TODO: Criar um dicionario de perguntas/alternativas
  print(teste)
  perguntas_dict = {}
  if request.method == 'GET':
    
    link = Link.objects.get(id=id)
    if link.expire_date < datetime.now().replace(tzinfo=utc):
      return render(request, 'disc_website/login.html')  
  
    for pergunta in Pergunta.objects.filter():
      perguntas_dict[pergunta.enunciado] = Alternativa.objects.filter(pergunta=pergunta)
    return render(request, "projeto5_website/teste.html",
              {"perguntas": perguntas_dict})
    
  elif request.method == 'POST':
    print(request.POST)
    totalRespostas = 0
    respostas_dict = {
      '1' : 0,
      '2' : 0,
      '3' : 0,
      '4' : 0,
    }
    ra = request.POST['ra']
    email = request.POST['email']
    nome =  request.POST['nome']
    empregado = 'empregadoOpcao' in request.POST
      
    print (request.POST)
    for chave, conteudo in request.POST.items():
      if chave not in ['csrfmiddlewaretoken','ra','email','nome','empregadoOpcao']:
        respostas_dict[conteudo[0]] += 1
        totalRespostas += 1

    for chave, conteudo in respostas_dict.items():
      respostas_dict[chave] = (respostas_dict[chave] / totalRespostas) * 100
      
    try:
      aluno = Aluno.objects.get(ra=ra)
    
    except Aluno.DoesNotExist:    
      aluno = Aluno()
      aluno.ra = ra
      aluno.email = email
      aluno.nome = nome
      aluno.empregado = empregado
      aluno.save()

    resultado = Resultado()
    for choice, nome in CHOICES_ALTERNATIVA:
      setattr(resultado, nome, respostas_dict[str(choice)])
    
    #pega o maior valor do dicionario de respostas e armazena na variável
    max_key = max(respostas_dict.items(), key=operator.itemgetter(1))[0]
    
    #laço de repetição para comparar a maior porcentagem das respostas com os valores da CHOICES_ALTERNATIVAS,
    #dessa forma será atribuido na variável o perfil predominante.
    for choice, nome in CHOICES_ALTERNATIVA:
        if max_key == str(choice):
          resultado.perfildominante = nome
        else:
          continue
    
    resultado.data_fim = resultado.data_ini = datetime.now()
    resultado.aluno = aluno
    resultado.save()

    print(respostas_dict)
    print(resultado.perfildominante)
    return render(request, "projeto5_website/teste.html",
              {"perguntas": perguntas_dict})
  
def instituicoes(request):
  return render(request, "projeto5_website/teste.html",
            {"instituicoes": Instituicao.objects.all()})
 
@login_required   
def resultados(request):
  # respostas_dict = {}
  # if request.method == 'GET':
  #   for resposta in Resultado.objects():
  #     respostas_dict[resposta] = Alternativa.objects.filter(pergunta=pergunta)

  return render(request, "projeto5_website/resultados.html",
            {"resultados": Resultado.objects.all()})
  

def obrigado(request):
  return render(request, "projeto5_website/obrigado.html",
            {"obrigado": Resultado.objects.all()})
