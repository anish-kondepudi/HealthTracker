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

function fieldComplete3(condition) {
  var x = document.getElementById("healthy");
  var y = document.getElementById("typeWorkout");
  var z = document.getElementById("workoutLength");
  if (condition == 0) {
    x.style.display = "block";
    y.style.display = "none";
    z.style.display = "none";
  }
  else if (condition == 1) {
    x.style.display = "none";
    y.style.display = "block";
    z.style.display = "block";
  }
}

function fieldComplete4() {
  var x = document.getElementById("healthy");
  if (x.style.display === "none") {
    x.style.display = "block";
  }
}

function fieldComplete5(condition) {
  var x = document.getElementById("unhealthyFood");
  var y = document.getElementById("proudAchievement");
  if (x.style.display === "none" && condition == 0) {
    x.style.display = "block";
    y.style.display = "none";
  }
  else if (y.style.display === "none" && condition == 1) {
    x.style.display = "none";
    y.style.display = "block";
  }
}

function fieldComplete6() {
  var x = document.getElementById("proudAchievement");
  if (x.style.display === "none") {
    x.style.display = "block";
  }
}

function fieldComplete7() {
  var x = document.getElementById("submitButton");
  if (x.style.display === "none") {
    x.style.display = "block";
  }
}