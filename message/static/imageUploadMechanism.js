
// // Get the element where the images will be displayed
// var previewArea = document.getElementById("preview-area");

// // Get the input element for file uploads
// var fileInput = document.getElementById("id_images");

// // Initialize an empty array to store the image files
// var imageFiles = [];

// // Add a change event listener to the file input
// fileInput.addEventListener("change", function (event) {
//     // Get the selected files
//     imageFiles = event.target.files;

//     // Reset the preview area
//     previewArea.innerHTML = '';

//     // Loop through each selected file
//     for (var i = 0; i < imageFiles.length; i++) {
//         var file = imageFiles[i];

//         // Preview the image using Fancybox
//         var reader = new FileReader();
//         reader.onload = (function (file) {
//             return function (event) {
//                 // Create a new div element for the thumbnail
//                 var thumbnail = document.createElement("div");
//                 thumbnail.className = "thumbnail";
//                 // Create a new link element for Fancybox
//                 var link = document.createElement("a");
//                 link.href = event.target.result;
//                 link.setAttribute("data-fancybox", "gallery");
//                 // Get the name of the image file
//                 var fileName = file.name;
//                 // Set the caption attribute with the image file name
//                 link.setAttribute("data-caption", fileName);
//                 // Create a new image element
//                 var image = document.createElement("img");
//                 image.src = event.target.result;
//                 // Append the image to the link
//                 link.appendChild(image);
//                 // Append the link to the thumbnail
//                 thumbnail.appendChild(link);
                
//                 // Create a new button element for deleting
//                 var button = document.createElement("button");
//                 button.className = "delete";
//                 button.textContent = "X";
//                 // Add a click event listener to the button
//                 button.addEventListener("click", function () {
//                     // Remove the thumbnail from the preview area
//                     previewArea.removeChild(thumbnail);
//                     // Remove the corresponding file from the list of files to be uploaded
//                     imageFiles = imageFiles.filter(function (imgFile) {
//                         return imgFile.name !== fileName;
//                     });
//                     // Update the file input value to reflect the changes
//                     fileInput.files = imageFiles;
//                 });

//                 // Append the button to the thumbnail
//                 thumbnail.appendChild(button);
//                 // Append the thumbnail to the preview area
//                 previewArea.appendChild(thumbnail);
//             };
//         })(file);
//         reader.readAsDataURL(file);
//     }
// });

// // Initialize the Fancybox plugin
// Fancybox.bind("[data-fancybox]", {
//     // Your custom options
// });


// Get the element where the images will be displayed
var previewArea = document.getElementById("preview-area");

// Get the input element for file uploads
var fileInput = document.getElementById("id_images");

// Add a change event listener to the file input
fileInput.addEventListener("change", function (event) {
    // Get the selected files
    var imageFiles = event.target.files;

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
