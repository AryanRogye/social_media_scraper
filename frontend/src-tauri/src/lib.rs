use std::fmt::format;
use std::io::BufRead;

// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

fn handle_txt(file: &str) -> Result<String, Box<dyn std::error::Error>> {
    println!("CALLED");
    // Read The Txt and
    use std::fs::File;
    use std::io::{self,BufRead};
    let f = File::open(file)?;
    let reader = io::BufReader::new(f);
    // Limit to opening 10 right now
    let mut count = 0;
    for line in reader.lines() {
        if count == 9 {
            break;
        }
        let line = line?;
        println!("{}", line);
        if let Err(e) = open::that(line) {
            eprintln!("There was a problem opening the file: {}", e);
        }
        count = count + 1;
    }
    Ok(String::from("Success"))
}
#[tauri::command]
fn parse_file(file: &str) -> String{
    // Check the extension first
    if file.ends_with(".txt") || file.ends_with(".log") {
        println!("Is A Txt Parsing Started");
        match handle_txt(file){
            Ok(..) => {},
            Err(e) => println!("There was an Error {}", e)
        }
    } else {
        return "Cant Parse This File Yet".to_string()
    }
    return "Parsing Done".to_string()
}
#[tauri::command]
fn open_finder() -> String {
    use rfd::FileDialog;
    if let Some(files) = FileDialog::new()
        .add_filter("text", &["txt", "json", "log"])
        .set_directory(".")
        .pick_file()
    {
        return format!("{}", files.to_string_lossy())
    } else {
        return format!("None")
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .invoke_handler(tauri::generate_handler![greet, open_finder, parse_file])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
