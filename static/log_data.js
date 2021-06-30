function fieldComplete1() {
  var x = document.getElementById("sleep");
  if (x.style.display === "none") {
    x.style.display = "block";
  }
}

function fieldComplete2() {
  var x = document.getElementById("workout");
  if (x.style.display === "none") {
    x.style.display = "block";
  }
}

function fieldComplete3(y) {

  var x = document.getElementById("healthy");
  if (x.style.display === "none") {
    x.style.display = "block";
  }

  x = document.getElementById("workoutFollowup");
  if (y) {
    x.style.display = "block";
  }
  else {
    console.log("NO");
    x.style.display = "none";
  }
}

function fieldComplete4() {
  var x = document.getElementById("workoutLength");
  if (x.style.display === "none") {
    x.style.display = "block";
  }
}

function fieldComplete5() {
  var x = document.getElementById("typeWorkout");
  if (x.style.display === "none") {
    x.style.display = "block";
  }
}

function fieldComplete6() {
  var x = document.getElementById("unhealthyFood");
  if (x.style.display === "none") {
    x.style.display = "block";
  }
}

function fieldComplete7() {
  var x = document.getElementById("proudAchievement");
  if (x.style.display === "none") {
    x.style.display = "block";
  }
}

function fieldComplete8() {
  var x = document.getElementById("submitButton");
  if (x.style.display === "none") {
    x.style.display = "block";
  }
}