document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#home-link").href = 'http://127.0.0.1:8000/'
    document.querySelector("#matches-link").href = 'http://127.0.0.1:8000/page/matches';
    document.querySelector("#about-link").href = 'http://127.0.0.1:8000/page/about';

    load_view("home");
})
function load_view(view) {
    if (view === "home") {
        document.querySelector("#home").style.display = "block";
        document.querySelector("#home-slide-show").style.display = "block";
        document.querySelector("#search").addEventListener("keyup", function(event){
            if (event.keyCode === 13) {
                event.preventDefault();
                document.querySelector("#searchbtn").click();
            }
        })
        document.querySelector("#searchbtn").addEventListener("click", function () {
            let query = document.querySelector("#search").value;
            if (query.length > 0) {
                window.location = `http://127.0.0.1:8000/search/${query}`;
            }
        })
        document.querySelector("#allbtn").addEventListener("click", function () {
            let query = "all";
            window.location = `http://127.0.0.1:8000/search/${query}`;
            })
    }
}
