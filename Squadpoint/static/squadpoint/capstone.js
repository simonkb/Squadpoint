document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("#home-link").href = 'https://squadpoint.herokuapp.com'
    document.querySelector("#matches-link").href = 'https://squadpoint.herokuapp.com';
    document.querySelector("#about-link").href = 'https://squadpoint.herokuapp.com';

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
                window.location = `https://squadpoint.herokuapp.com/search/${query}`;
            }
        })
        document.querySelector("#allbtn").addEventListener("click", function () {
            let query = "all";
            window.location = `https://squadpoint.herokuapp.com/search/${query}`;
            })
    }
}
