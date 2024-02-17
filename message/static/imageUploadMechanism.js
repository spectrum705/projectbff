
// Get the element where the images will be displayed
var previewArea = document.getElementById("preview-area");

// Get the input element for file uploads
var fileInput = document.getElementById("id_images");

// Add a change event listener to the file input
fileInput.addEventListener("change", function (event) {
    // Get the selected files
    var imageFiles = event.target.files;
    
    
     // Check if the number of selected images exceeds 12
     if (imageFiles.length > 12) {
        // Display a warning pop-up message
        alert("You can only upload up to 12 images. Please re-upload.");

        // Clear the file input field
        event.target.value = "";
        return;
    }

    // Reset the preview area
    previewArea.innerHTML = '';

    // Loop through each selected file
    for (var i = 0; i < imageFiles.length; i++) {
        var file = imageFiles[i];

        // Preview the image using Fancybox
        var reader = new FileReader();
        reader.onload = (function (file) {
            return function (event) {
                // Create a new div element for the thumbnail
                var thumbnail = document.createElement("div");
                thumbnail.className = "thumbnail";
                // Create a new link element for Fancybox
                var link = document.createElement("a");
                link.href = event.target.result;
                link.setAttribute("data-fancybox", "gallery");
                // Get the name of the image file
                var fileName = file.name;
                // Set the caption attribute with the image file name
                link.setAttribute("data-caption", fileName);
                // Create a new image element
                var image = document.createElement("img");
                image.src = event.target.result;
                image.setAttribute("loading","lazy")
                image.setAttribute("width","300")
                image.setAttribute("height","300")

                // Append the image to the link
                link.appendChild(image);
                // Append the link to the thumbnail
                thumbnail.appendChild(link);
                // Append the thumbnail to the preview area
                previewArea.appendChild(thumbnail);
            };
        })(file);
        reader.readAsDataURL(file);
    }
});

// Initialize the Fancybox plugin
Fancybox.bind("[data-fancybox]", {
    // Your custom options
});

