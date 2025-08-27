    const input = document.getElementById('image');
    const preview = document.getElementById('preview');
    const dropzone = document.getElementById('dropzone');

    function showPreview(file) {
      if (!file || !file.type.startsWith('image/')) return;
      const url = URL.createObjectURL(file);
      preview.src = url;
      preview.style.display = 'block';
      dropzone.classList.add('has-preview');
    }
    input.addEventListener('change', e => showPreview(e.target.files[0]));
    ['dragenter','dragover'].forEach(ev =>
      dropzone.addEventListener(ev, e => { e.preventDefault(); dropzone.classList.add('drag'); })
    );
    ['dragleave','drop'].forEach(ev =>
      dropzone.addEventListener(ev, e => { e.preventDefault(); dropzone.classList.remove('drag'); })
    );
    dropzone.addEventListener('drop', e => {
      const file = e.dataTransfer.files[0];
      if (file) { input.files = e.dataTransfer.files; showPreview(file); }
    });

    function dismissAlert() {
    const alertBox = document.getElementById("alertBox");
    if (alertBox) {
        alertBox.style.display = "none";
        }
    }