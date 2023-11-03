from django.http import HttpResponse
from langchain.vectorstores import Chroma
from django.conf import settings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os
from django.shortcuts import render
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Cluster
from .forms import ClusterForm
from django.shortcuts import render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from .utils import embedding_function


def getReply(request,cluster_id):
    if request.method == "GET":
        print(request.GET)
        # embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        try:
            question = request.GET.get('q', '')
            cluster = get_object_or_404(Cluster, id=cluster_id)
            # embedding_function = OpenAIEmbeddings(openai_api_key=cluster.openai_api_key)
            db_path = os.path.join(settings.BASE_DIR, cluster.chroma_db_directory)
            print(db_path)
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
    url=get_current_site(request)
    user_clusters = Cluster.objects.filter(user=request.user)
    
    context = {
        'user_clusters': user_clusters,
        'url':url
    }
    return render(request, 'myapp/profile.html', context)
    
@login_required
def create_cluster(request):
    if request.method == 'POST':
        form = ClusterForm(request.POST, request.FILES)
        if form.is_valid():
            form.user=request.user
        
            cluster = form.save(commit=False)
            
            cluster.save()

            print("Cluster ID: ",cluster.id)
            chroma_db_subdirectory = str(cluster.id)
            chroma_db_path = os.path.join(settings.BASE_DIR, 'chroma_db', chroma_db_subdirectory)
            os.makedirs(chroma_db_path, exist_ok=True)
            
            uploaded_txt = form.cleaned_data['txt_file']
            with open('temp.txt', 'wb') as temp_file:
                for chunk in uploaded_txt.chunks():
                    temp_file.write(chunk)


            loader = TextLoader("temp.txt",'utf8')
            documents = loader.load()
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            docs = text_splitter.split_documents(documents)
            # embedding_function = cluster.embedding_function
            # embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            # embedding_function = OpenAIEmbeddings(openai_api_key=cluster.openai_api_key)
            vectordb = Chroma.from_documents(documents=docs, embedding=embedding_function, persist_directory=chroma_db_path)
            vectordb.persist()
            print(chroma_db_subdirectory)
            print(chroma_db_path)
            cluster.chroma_db_directory = chroma_db_path
            cluster.save()
            return redirect('/profile/')
    else:
        form = ClusterForm()
    return render(request, 'myapp/create_cluster.html', {'form': form})


# def cluster_details(request, cluster_id):
#     cluster = get_object_or_404(Cluster, id=cluster_id)
#     # You can add more context data or logic here
#     return render(request, 'myapp/cluster_details.html', {{'cluster': cluster}})

from .forms import UpdateTxtFileForm
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

class UpdateClusterTxtFileView(UpdateView):
    model = Cluster
    form_class = UpdateTxtFileForm
    template_name = 'myapp/update.html'  # Create an HTML template for updating txt_file
    success_url = reverse_lazy('profile')  # Redirect to the profile page after successful update

    def form_valid(self, form):
        # Set the user of the Cluster instance to the logged-in user
        form.instance.user = self.request.user
        # form.save()
        cluster = form.save(commit=False)
        cluster.save()
        
        chroma_db_subdirectory = str(cluster.id)
        chroma_db_path = os.path.join(settings.BASE_DIR, 'chroma_db', chroma_db_subdirectory)
        os.makedirs(chroma_db_path, exist_ok=True)
        
        uploaded_txt = form.cleaned_data['txt_file']
        with open('temp.txt', 'wb') as temp_file:
            for chunk in uploaded_txt.chunks():
                temp_file.write(chunk)


        loader = TextLoader("temp.txt",'utf8')
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        # embedding_function = cluster.embedding_function
        # embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        # embedding_function = OpenAIEmbeddings(openai_api_key=cluster.openai_api_key)
        vectordb = Chroma.from_documents(documents=docs, embedding=embedding_function, persist_directory=chroma_db_path)
        vectordb.persist()
        print(chroma_db_subdirectory)
        print(chroma_db_path)
        cluster.chroma_db_directory = chroma_db_path
        cluster.save()        
        return super().form_valid(form)
    


def deletebot(request, cluster_id):
    cluster = get_object_or_404(Cluster, id=cluster_id)

        # Clean up any associated data or files if needed (similar to the model's delete method)
        # Example: Delete the associated txt_file
    if cluster.txt_file:
        cluster.txt_file.delete()

    cluster.delete()
    return redirect('profile')


def gettemplate(request, cluster_id):
    cluster = get_object_or_404(Cluster, id=cluster_id)

        # Clean up any associated data or files if needed (similar to the model's delete method)
        # Example: Delete the associated txt_file
    url=str(get_current_site(request))+cluster.get_absolute_url
    
    html="""
    <div class="chat-container">
        <div class="chat-log" id="chat-log">
        </div>
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Type your message...">
            <button id="send-button">Send</button>
        </div>
    </div>
    """ 

    js = f"""
    document.addEventListener('DOMContentLoaded', function() {{
        const chatLog = document.getElementById('chat-log');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');

        function addMessage(user, message) {{
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            messageDiv.innerHTML = `<strong>${{user}}:</strong> ${{message}}`;
            chatLog.appendChild(messageDiv);
            chatLog.scrollTop = chatLog.scrollHeight;
        }}

        sendButton.addEventListener('click', function() {{
            const userMessage = userInput.value.trim();

            if (userMessage) {{
                addMessage('User', userMessage);
                userInput.value = '';

                let request = new XMLHttpRequest();
                request.open("GET", `{url}?q=${{userMessage}}`);
                request.send();
                request.onload = () => {{
                    if (request.status == 200) {{
                        let data = request.response + '<br><br>';
                        console.log(data)
                        addMessage('Chatbot', data);
                    }}
                }}
            }}
        }});

        // Handle Enter key press
        userInput.addEventListener('keydown', function(event) {{
            if (event.key === 'Enter') {{
                sendButton.click();
            }}
        }});
    }});
"""
    
    css="""
body {
    font-family: Arial, sans-serif;
}

.chat-container {
    max-width: 400px;
    margin: 0 auto;
    border: 1px solid #ccc;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px #ccc;
}

.chat-log {
    height: 70vh;
    overflow-y: scroll;
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 5px;
}

.input-container {
    display: flex;
}

#user-input {
    flex: 1;
    padding: 5px;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-right: 10px;
}

#send-button {
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    cursor: pointer;
}

#send-button:hover {
    background-color: #0056b3;
}
"""

    context = {
        'html':html,
        'js':js,
        'css':css,
        'url':url
    }

    return render(request, 'myapp/getTemplate.html', context)

