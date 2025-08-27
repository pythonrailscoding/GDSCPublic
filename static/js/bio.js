
document.addEventListener("DOMContentLoaded", function() {
  const bioText = document.getElementById("bio-text");
  const btn = document.getElementById("view-more-btn");

  const collapsedHeight = 150; // same as CSS max-height

  if (bioText.scrollHeight <= collapsedHeight) {
    // Bio is short, no need for button
    btn.style.display = "none";
  }

  btn.addEventListener("click", () => {
    bioText.classList.toggle("expanded");
    btn.textContent = bioText.classList.contains("expanded")
      ? "View Less"
      : "View More";
  });
});

