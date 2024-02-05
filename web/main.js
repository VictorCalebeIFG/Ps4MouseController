eel.python_print("hello");
eel.python_get_active_window();

var screen_index = 0;

let controller_buttons = document.getElementsByClassName("controller-buttons")[0];
let screen_list = document.getElementsByClassName("screen-list")[0];

async function readJsonFile() {
    let controller_mapping =  JSON.stringify( await eel.get_json_file("input_mapping")());
    let mapping = JSON.parse(controller_mapping);

    eel.python_print(mapping['left-mouse']);   
}

function set_mouse_speed(){
    var mouse_speed = document.getElementById("mouse-speed").value;
    eel.python_set_speed(mouse_speed);
    eel.python_print(mouse_speed);
}

eel.expose(render_screen_list);
async function render_screen_list() {
    let list_to_render = await eel.python_get_windows()()

    let screenListDiv = document.querySelector('.screen-list');
    screenListDiv.innerHTML = "";

    list_to_render.forEach(element => {
        let new_li = document.createElement('li');
        new_li.innerHTML = element;
        screenListDiv.appendChild(new_li);
    });

    let list_elements = document.querySelectorAll('.screen-list li');
    list_elements[screen_index].classList.add('selected');
}

eel.expose(js_select_screen_ui);
function js_select_screen_ui(action){
    let list_elements = document.querySelectorAll('.screen-list li');
    list_elements[screen_index].classList.remove('selected');

    if (action == "up"){
        screen_index = screen_index - 1;
    } else if (action == "down"){
        screen_index = screen_index + 1;
    }
    if (screen_index < 0){
        screen_index = 0;
    } else if (screen_index > list_elements.length - 1){
        screen_index = list_elements.length - 1;
    }

    list_elements[screen_index].classList.add('selected');
    list_elements[screen_index].scrollIntoView();
    
}

eel.expose(js_get_screen_selected);
function js_get_screen_selected(){
    let list_elements = document.querySelectorAll('.screen-list li');
    return list_elements[screen_index].innerHTML;
}

eel.expose(js_arrow_up);
function js_arrow_up(){
    console.log("js_arrow_up")
}



readJsonFile();
render_screen_list();