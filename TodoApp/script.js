function addTask() {
  const input = document.getElementById("taskInput");
  const taskText = input.value.trim();
  if (taskText === "") return;

  const li = document.createElement("li");
  li.textContent = taskText;

  li.onclick = () => li.classList.toggle("completed"); // mark complete

  const deleteBtn = document.createElement("button");
  deleteBtn.textContent = "X";
  deleteBtn.onclick = () => li.remove(); // delete task

  li.appendChild(deleteBtn);
  document.getElementById("taskList").appendChild(li);

  input.value = ""; // clear input
}
function toggleDarkMode() {
  document.body.classList.toggle("dark");
}
function addTask() {
  const input = document.getElementById("taskInput");
  const taskText = input.value.trim();
  if (taskText === "") return;

  const li = document.createElement("li");
  li.textContent = taskText;

  li.onclick = () => {
    li.classList.toggle("completed");
    saveTasks();
  };

  const deleteBtn = document.createElement("button");
  deleteBtn.textContent = "X";
  deleteBtn.onclick = () => {
    li.remove();
    updateTaskCount();
    saveTasks();
  };

  li.appendChild(deleteBtn);
  document.getElementById("taskList").appendChild(li);
  input.value = "";

  updateTaskCount();
  saveTasks(); // Save after adding
}
function saveTasks() {
  const tasks = [];
  const listItems = document.querySelectorAll('#taskList li');
  listItems.forEach(li => {
    tasks.push({
      text: li.firstChild.textContent,
      completed: li.classList.contains("completed")
    });
  });
  localStorage.setItem("tasks", JSON.stringify(tasks));
}

function loadTasks() {
  const saved = JSON.parse(localStorage.getItem("tasks") || "[]");
  saved.forEach(task => {
    const li = document.createElement("li");
    li.textContent = task.text;
    if (task.completed) li.classList.add("completed");

    li.onclick = () => {
      li.classList.toggle("completed");
      saveTasks();
    };

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "X";
    deleteBtn.onclick = () => {
      li.remove();
      updateTaskCount();
      saveTasks();
    };

    li.appendChild(deleteBtn);
    document.getElementById("taskList").appendChild(li);
  });
  updateTaskCount();
}
window.onload = loadTasks;
