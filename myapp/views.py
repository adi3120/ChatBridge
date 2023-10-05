from django.http import HttpResponse
from langchain.vectorstores import Chroma
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from django.conf import settings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os
from django.shortcuts import render
from django.contrib import messages
from django.views import View
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Cluster

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def getReply(request):
    if request.method == "GET":
        print(request.GET)
        global embedding_function

        try:
            question = request.GET.get('q', '')
            db_path = os.path.join(settings.BASE_DIR, 'myapp\chroma_db')
            if os.path.exists(db_path) and os.path.isdir(db_path):
                db3 = Chroma(persist_directory=db_path, embedding_function=embedding_function)
                docs = db3.similarity_search(question)
            else:
                print("Directory 'chroma_db' not found")
        except Exception as e:
            print("Error:", e)
            docs = []

    return HttpResponse(docs[0].page_content)

def home(request):
    return render(request, "myapp/home.html")

class register(View):
	def get(self,request):
		form=RegistrationForm()
		context={
			'form':form
		}
		return render(request, 'myapp/register.html',context)
	def post(self,request):
		form=RegistrationForm(request.POST)
		if form.is_valid():
			messages.success(request,"Congratulations!! Registered Successfully")
			form.save()
		context={
			'form':form
		}
		return render(request, 'myapp/register.html',context)
     
@login_required
def profile(request):
    user_clusters = Cluster.objects.filter(user=request.user)
    context = {
        'user_clusters': user_clusters
    }
    return render(request, 'myapp/profile.html', context)
    
from .forms import ClusterForm
@login_required
def create_cluster(request):
    if request.method == 'POST':
        form = ClusterForm(request.POST, request.FILES)
        if form.is_valid():
            cluster = form.save(commit=False)  # Create the cluster instance but don't save it yet
            cluster.user = request.user  # Set the user to the logged-in user
            cluster.save()  # Save the cluster instance with the user
            return redirect('/profile/')  # Redirect to a success page
    else:
        form = ClusterForm()
    return render(request, 'myapp/create_cluster.html', {'form': form})

