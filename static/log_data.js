function fieldComplete1() {
  document.getElementById("sleep").style.display = "block";
}

function fieldComplete2() {
  document.getElementById("workout").style.display = "block";
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
    y.style.display = "block";
    z.style.display = "block";
  }
}

function fieldComplete4() {
  document.getElementById("healthy").style.display = "block";
}

function fieldComplete5(condition) {
  var x = document.getElementById("unhealthyFood");
  var y = document.getElementById("proudAchievement");
  if (condition == 0) {
    x.style.display = "block";
  }
  else if (condition == 1) {
    x.style.display = "none";
    y.style.display = "block";
  }
}

function fieldComplete6() {
  document.getElementById("proudAchievement").style.display = "block";
}

function fieldComplete7() {
  document.getElementById("submitButton").style.display = "block";
}