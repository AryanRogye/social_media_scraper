// Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
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
        .invoke_handler(tauri::generate_handler![greet, open_finder])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
