window.addEventListener("load", function () {
    if (document.documentElement.classList.contains("skip-loader")) return;

    const loader = document.getElementById("loader");

    // Show for 3s only on first visit
    setTimeout(() => {
        loader.style.opacity = "0"; // fade out
        setTimeout(() => {
            loader.style.display = "none";
            sessionStorage.setItem("loaderShown", "true");
            // Difference between sessionstorage and localstorage.
            // SessionStorage is limited to memory in one tab
            // Localstorage limits to that browser storage. Clear cache and remove it
        }, 500);
    }, 3000);
});
