// The problem we were facing in Javascript was 400 bad request as in backend we were expecting a form and from here we were sending just naive data so after wrapping it in a form it worked. So we need to make sure we send the same type request data the backend is structured. 
window.onload = function() {
  //var url = "http://127.0.0.1:5000/get_location_names"
  //  var url = "/api/get_location_names";
   var url = "http://ec2-16-171-25-63.eu-north-1.compute.amazonaws.com/api/get_location_names"
  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then(data => {
      const locationSelect = document.getElementById("location");
      locationSelect.innerHTML = '<option value="" disabled selected>Select Location</option>';
      data.locations.forEach(loc => {
        const option = document.createElement("option");
        option.value = loc;
        option.textContent = loc;
        locationSelect.appendChild(option);
      });
    })
    .catch(error => {
      console.error("Error fetching locations:", error);
      const locationSelect = document.getElementById("location");
      locationSelect.innerHTML = '<option value="" disabled selected>Failed to load locations</option>';
    });
};
  
// Handle form submission
document.getElementById("price-form").addEventListener("submit", function(e) {
  e.preventDefault(); // Prevent default form submission

  // Get form values
  const total_sqft = parseFloat(document.getElementById("total_sqft").value);
  const bath = parseInt(document.getElementById("bathrooms").value);
  const balcony = parseInt(document.getElementById("balconies").value);
  const bhk = parseInt(document.getElementById("bhk").value);
  const location = document.getElementById("location").value;

  // Ensure all fields are filled before sending the request
  if (!total_sqft || !bath || !balcony || !bhk || !location) {
    alert("Please fill in all the fields.");
    return;
  }

  // Prepare data for POST using user input
  const data = new FormData();
  data.append('location', location);   // Use location from the form
  data.append('total_sqft', total_sqft);  // Use total_sqft from the form
  data.append('bhk', bhk);             // Use bhk from the form
  data.append('bath', bath);           // Use bath from the form
  data.append('balcony', balcony);     // Use balcony from the form
  
  // Make the API request

    //var url = "predict_home_price"
    //var url = "/api/predict_home_price"
     var url = "http://ec2-16-171-25-63.eu-north-1.compute.amazonaws.com/api/predict_home_price"
  fetch(url, {
    method: "POST",
    body: data, // Sending FormData with the actual user data
  })
  .then(response => response.json()) // Parse JSON response
  .then(result => {
    // Handle the result
    const resultBox = document.getElementById("result");
    resultBox.textContent = `Estimated Price: ₹ ${result.estimated_price.toLocaleString()}`;
  })
  .catch(error => {
    console.error("Prediction error:", error);
    document.getElementById("result").textContent = "Failed to get prediction. Please try again.";
  });

});
