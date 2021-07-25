const html = document.documentElement;
const body = document.body;
const menuLinks = document.querySelectorAll(".admin-menu a");
const collapseBtn = document.querySelector(".admin-menu .collapse-btn");
const toggleMobileMenu = document.querySelector(".toggle-mob-menu");
const switchInput = document.querySelector(".switch input");
const switchLabel = document.querySelector(".switch label");
const switchLabelText = switchLabel.querySelector("span:last-child");
const collapsedClass = "collapsed";
const lightModeClass = "light-mode";

/*TOGGLE HEADER STATE*/
collapseBtn.addEventListener("click", function () {
    body.classList.toggle(collapsedClass);
    this.getAttribute("aria-expanded") == "true"
        ? this.setAttribute("aria-expanded", "false")
        : this.setAttribute("aria-expanded", "true");
    this.getAttribute("aria-label") == "collapse menu"
        ? this.setAttribute("aria-label", "expand menu")
        : this.setAttribute("aria-label", "collapse menu");
});

/*TOGGLE MOBILE MENU*/
toggleMobileMenu.addEventListener("click", function () {
    body.classList.toggle("mob-menu-opened");
    this.getAttribute("aria-expanded") == "true"
        ? this.setAttribute("aria-expanded", "false")
        : this.setAttribute("aria-expanded", "true");
    this.getAttribute("aria-label") == "open menu"
        ? this.setAttribute("aria-label", "close menu")
        : this.setAttribute("aria-label", "open menu");
});

/*SHOW TOOLTIP ON MENU LINK HOVER*/
for (const link of menuLinks) {
    link.addEventListener("mouseenter", function () {
        if (
            body.classList.contains(collapsedClass) &&
            window.matchMedia("(min-width: 768px)").matches
        ) {
            const tooltip = this.querySelector("span").textContent;
            this.setAttribute("title", tooltip);
        } else {
            this.removeAttribute("title");
        }
    });
}

/*TOGGLE LIGHT/DARK MODE*/
if (localStorage.getItem("dark-mode") === "false") {
    html.classList.add(lightModeClass);
    switchInput.checked = false;
    switchLabelText.textContent = "Light";
}

switchInput.addEventListener("input", function () {
    html.classList.toggle(lightModeClass);
    if (html.classList.contains(lightModeClass)) {
        switchLabelText.textContent = "Light";
        localStorage.setItem("dark-mode", "false");
    } else {
        switchLabelText.textContent = "Dark";
        localStorage.setItem("dark-mode", "true");
    }
});



function openpopbar() {
    document.querySelector(".popup-bar").style.display = "flex";
}
function openpoppie() {
    document.querySelector(".popup-pie").style.display = "flex";
}
function openpopline() {
    document.querySelector(".popup-line").style.display = "flex";
}
function openpopcard() {
    document.querySelector(".popup-card").style.display = "flex";
}

function closesbar() {

    document.querySelector(".popup-bar").style.display = "none";
}
function closespie() {

    document.querySelector(".popup-pie").style.display = "none";
}
function closesline() {

    document.querySelector(".popup-line").style.display = "none";
}
function closescard() {

    document.querySelector(".popup-card").style.display = "none";
}
function opens() {

    document.querySelector(".popup").style.display = "none";
    document.write("hahah");
}
function myFunction1() {
    var x = document.getElementById("myDIV1");
    var y = document.getElementById("myDIV2");
    if (x.style.display === "none") {
        y.style.display = "none";
        x.style.display = "block";
    }
}
function myFunction2() {
    var x = document.getElementById("myDIV1");
    var y = document.getElementById("myDIV2");
    if (y.style.display === "none") {
        x.style.display = "none";
        y.style.display = "block";
    }

}

function editreport() {
    var e = document.getElementById("Edit_btn");
    var save = document.getElementById("Save_btn");
    save.style.display = "block";
    s.style.display = "block";
    e.style.display = "none";
}