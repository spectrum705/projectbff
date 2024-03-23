
// Get the element where the images will be displayed
var previewArea = document.getElementById("preview-area");

// Get the input element for file uploads
var fileInput = document.getElementById("id_images");

// Add a change event listener to the file input
fileInput.addEventListener("change", function (event) {
    // Get the selected files
    // var maxSize = 4 * 1024 * 1024;
    
    
    var totalSizeLimit = 19 * 1024 * 1024; // 4.5 MB in bytes
    var totalSize = 0;
    var imageFiles = event.target.files;
    var allowedTypes = ['image/jpeg','image/jpg', 'image/png', 'image/gif'];

    
    console.log("Total selected files:", imageFiles.length);
    // Iterate over each selected file to calculate the total size
    for (var i = 0; i < imageFiles.length; i++) {
        totalSize += imageFiles[i].size; // Add the size of each file to the total size
        console.log("File size:", totalSize,"/",totalSizeLimit);
            // Check if the file type is allowed
       
             // Check if the file type is allowed
        if (!allowedTypes.includes(imageFiles[i].type)) {
            alert("Unsupported file type. Please upload images in JPG, PNG, or GIF format.");
            event.target.value = ""; // Clear the file input field
            return;
        }



        }

    // Check if the total size exceeds the limit
    if (totalSize > totalSizeLimit) {
        // Display a warning pop-up message
        
        alert("Limit exceeded. You can only upload upto 20mb of images In total.");
        
        // Clear the file input field
        event.target.value = "";
        return;
    }


    
     // Check if the number of selected images exceeds 12
     if (imageFiles.length > 8) {
        // Display a warning pop-up message
        alert("You can only upload up to 8 images. Please re-upload.");

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

