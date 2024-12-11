function showInput(type) {
    
    document.getElementById("inputText").style.display = "none";
    document.getElementById("ocrFile").style.display = "none";
    document.getElementById("submit").style.display = "none";

    if (type === 'text') {
        document.getElementById("inputLang").defaultValue = "auto";
        document.getElementById("inputText").style.display = "block";
    } else if (type === 'file') {
        document.getElementById("ocrFile").style.display = "block";
        document.getElementById("submit").style.display = "block";
    }
}

async function uploadFileForOCR() {
    const fileInput = document.getElementById("ocrFile");
    const inputLang = document.getElementById("inputLang").value || "auto";
    const outputLang = document.getElementById("outputLang").value || "hi";

    if (!fileInput.files[0]) {
        alert("Please choose a file before submitting.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("inputLang", inputLang);
    formData.append("outputLang", outputLang);

    try {
        const response = await fetch('/ocr', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (data.error) {
            console.error("Error during OCR:", data.error);
        } else {
            console.log("Extracted Text:", data.extracted_text);
            console.log("Translated Text:", data.translated_text);
            document.getElementById("outputText").value = data.translated_text;
        }
    } catch (error) {
        console.error("Error uploading file:", error);
    }
}

async function translateText() {
    const inputText = document.getElementById("inputText").value;
    const inputLang = document.getElementById("inputLang").value || "auto";
    const outputLang = document.getElementById("outputLang").value || "hi";

    try {
        const response = await fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: inputText, source: inputLang, target: outputLang }),
        });

        if (!response.ok) {
            console.error("Error with translation request:", response.status);
            return;
        }

        const data = await response.json();
        document.getElementById("outputText").value = data.translation;
    } catch (error) {
        console.error("Error translating text:", error);
    }
}
