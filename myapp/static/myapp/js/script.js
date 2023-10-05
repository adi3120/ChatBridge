function getReply() {
    let question = document.getElementById('questionInput').value
    if (question) {
        let request = new XMLHttpRequest();
        request.open("GET", "http://localhost:8000/getAnswer?q=" + question);
        request.send();
        request.onload = () => {
            if (request.status == 200) {
                let data = request.response;
                document.getElementById("answer").innerText = data
            }
        }
    }
}