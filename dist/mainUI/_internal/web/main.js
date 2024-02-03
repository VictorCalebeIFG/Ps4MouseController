eel.python_print("hello");
eel.python_get_active_window();

let controller_buttons = document.getElementsByClassName("controller-buttons")[0];

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

function set_controller_option() {
    var controller_option = document.getElementById("controller-option");
    eel.python_print(controller_option.value);
    if (controller_option.value == "ps4") {
        document.getElementById("left-mouse").innerHTML = "cross-button";
        document.getElementById("right-mouse").innerHTML = "square-button";
        document.getElementById("esc").innerHTML = "circle-button";
        document.getElementById("ctrl-tab").innerHTML = "R1";
        document.getElementById("ctrl-shift-tab").innerHTML = "L1";
        document.getElementById("grid-up").innerHTML = "direction-up";
        document.getElementById("grid-down").innerHTML = "direction-down";
        document.getElementById("grid-left").innerHTML = "direction-left";
        document.getElementById("grid-right").innerHTML = "direction-right";

    }
}


readJsonFile();
set_controller_option();