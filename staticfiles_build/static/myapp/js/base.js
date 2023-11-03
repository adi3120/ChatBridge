const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

const randomChar = () => chars[Math.floor(Math.random() * (chars.length - 1))],
    randomString = length => Array.from(Array(length)).map(randomChar).join("");

const main = document.querySelector(".main");
console.log(main)
const card = main.querySelector(".card");
const letters = card.querySelector(".card-letters");

const fontSize = parseInt(getComputedStyle(letters).fontSize, 7);
const viewportWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
const viewportHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
const maxChars = Math.floor((viewportWidth / fontSize) * (viewportHeight / fontSize));

const handleOnMove = e => {
    const rect = card.getBoundingClientRect(),
        x = e.clientX - rect.left,
        y = e.clientY - rect.top;

    letters.style.setProperty("--x", `${x}px`);
    letters.style.setProperty("--y", `${y}px`);

    letters.innerText = randomString(maxChars);
}
card.onmousemove = e => handleOnMove(e);

card.ontouchmove = e => handleOnMove(e.touches[0]);


(function() {

    document.addEventListener('DOMContentLoaded', function(event) {

        var list = document.querySelectorAll('.make-snippet');

        [].forEach.call(list, function(el) {
            var snippet = el.innerHTML.replace(/</g, '&lt;');
            snippet = snippet.replace(/ /g, '&nbsp;');
            var code = '<pre class="language-markup"><code>' + snippet + '</pre></code>';
            el.insertAdjacentHTML('afterend', code);
        });

        // if your page has prism.js you get syntax highlighting
        if (window.Prism) {
            Prism.highlightAll(false);
        }

    });

})();