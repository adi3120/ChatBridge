const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

const randomChar = () => chars[Math.floor(Math.random() * (chars.length - 1))],
    randomString = length => Array.from(Array(length)).map(randomChar).join("");

const main = document.querySelector(".main");
console.log(main)

const profilecontainer = main.querySelector(".profilecontainer");
console.log(profilecontainer)

const created = profilecontainer.querySelector(".created");
console.log(created)

const chatbot = created.querySelector(".chatbot");
console.log(chatbot)

const profilecard = chatbot.querySelector(".profilecard");
console.log(profilecard)

const profileletters = profilecard.querySelector(".profilecard-letters");
console.log(profileletters)


const profilefontSize = parseInt(getComputedStyle(profileletters).fontSize, 7);
const profileviewportWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
const profileviewportHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
const profilemaxChars = Math.floor((profileviewportWidth / profilefontSize) * (profileviewportHeight / profilefontSize));

const profilehandleOnMove = e => {
    console.log("moved");
    const rect = profilecard.getBoundingClientRect(),
        x = e.clientX - rect.left,
        y = e.clientY - rect.top;

    profileletters.style.setProperty("--x", `${x}px`);
    profileletters.style.setProperty("--y", `${y}px`);

    profileletters.innerText = randomString(profilemaxChars);
}
profilecard.onmousemove = e => profilehandleOnMove(e);

profilecard.ontouchmove = e => profilehandleOnMove(e.touches[0]);