
document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll(".dropdown").forEach(drop => {
    let btn = drop.querySelector(".icon-btn");
    btn.addEventListener("click", e => {
      e.stopPropagation();
      drop.classList.toggle("open");

      // close others
      document.querySelectorAll(".dropdown").forEach(d => {
        if (d !== drop) d.classList.remove("open");
      });
    });
  });

  // Close dropdowns on outside click
  document.addEventListener("click", () => {
    document.querySelectorAll(".dropdown").forEach(d => d.classList.remove("open"));
  });
});

