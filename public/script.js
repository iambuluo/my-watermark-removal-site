document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('imageInput');
    const maskInput = document.getElementById('maskInput');
    const imagePreview = document.getElementById('imagePreview');
    const maskPreview = document.getElementById('maskPreview');
    const imagePlaceholder = document.getElementById('imagePlaceholder');
    const maskPlaceholder = document.getElementById('maskPlaceholder');
    const processBtn = document.getElementById('processBtn');
    const statusArea = document.getElementById('statusArea');
    const statusText = document.getElementById('statusText');
    const resultArea = document.getElementById('resultArea');
    const resultImage = document.getElementById('resultImage');
    const downloadBtn = document.getElementById('downloadBtn');

    // Helper to preview image
    function previewFile(input, imgEl, placeholderEl) {
        input.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    imgEl.src = e.target.result;
                    imgEl.classList.remove('hidden');
                    placeholderEl.classList.add('hidden');
                };
                reader.readAsDataURL(file);
            } else {
                imgEl.classList.add('hidden');
                placeholderEl.classList.remove('hidden');
            }
        });
    }

    previewFile(imageInput, imagePreview, imagePlaceholder);
    previewFile(maskInput, maskPreview, maskPlaceholder);

    processBtn.addEventListener('click', async () => {
        if (!imageInput.files[0] || !maskInput.files[0]) {
            alert('Please select both an image and a mask.');
            return;
        }

        // Reset UI
        processBtn.disabled = true;
        processBtn.classList.add('opacity-50', 'cursor-not-allowed');
        statusArea.classList.remove('hidden');
        statusText.textContent = 'Processing... This may take up to 60s for cold start.';
        resultArea.classList.add('hidden');

        const formData = new FormData();
        formData.append('image', imageInput.files[0]);
        formData.append('mask', maskInput.files[0]);
        formData.append('hd_strategy', 'Original');
        formData.append('ldm_steps', '50');
        formData.append('prompt', '');

        try {
            const response = await fetch('/api/inpaint', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Processing failed');
            }

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            
            resultImage.src = url;
            downloadBtn.href = url;
            resultArea.classList.remove('hidden');
            
            // Scroll to result
            resultArea.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error(error);
            alert(`Error: ${error.message}`);
        } finally {
            processBtn.disabled = false;
            processBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            statusArea.classList.add('hidden');
        }
    });
});
