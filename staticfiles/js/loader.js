window.addEventListener("load", function () {
    if (document.documentElement.classList.contains("skip-loader")) return;

    const loader = document.getElementById("loader");

    // Show for 3s only on first visit
    setTimeout(() => {
        loader.style.opacity = "0"; // fade out
        setTimeout(() => {
            loader.style.display = "none";
            sessionStorage.setItem("loaderShown", "true");
        }, 500);
    }, 3000);
});
