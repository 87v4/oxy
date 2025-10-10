# Oxy - Discord Rich Presence GUI

Oxy is a sleek and user-friendly desktop application to create and manage Discord Rich Presence configurations. Easily customize your presence details, save/load profiles, and switch themes — all without writing code!

---

## Features

- Intuitive GUI with light and dark themes (powered by [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap))
- Manage multiple profiles with save/load functionality
- Supports all common Discord Rich Presence fields:
  - Details, State
  - Large & Small Images with hover text (small image optional)
- Automatic Discord RPC connection and presence updates
- Scrollable form for better usability on smaller screens
- Status display and graceful disconnect on exit
- Version display in the corner for easy tracking

---

## Installation

1. **Download the latest executable** from the [Releases](https://github.com/yourusername/oxy/releases) page (Windows `.exe`).

2. Alternatively, build from source:

```bash
git clone https://github.com/yourusername/oxy.git
cd oxy
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
python oxyv1.py
````

---

## Usage

1. Launch the app.
2. Enter your Discord Application Client ID.
3. Fill out presence details and images.
4. Save profiles for quick reuse.
5. Click **Start Presence** to activate your Rich Presence.
6. Use the theme selector to toggle light/dark mode.
7. Profiles and settings are saved in the `profiles` folder.

---

## Building the Executable

To create a standalone Windows executable:

```bash
pyinstaller --onefile --windowed --name oxy oxyv1.py
```

The output `.exe` will be located in the `dist` folder.

---

## Requirements

* Python 3.8+
* [pypresence](https://github.com/qwertyquerty/pypresence)
* [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)

Install dependencies via:

```bash
pip install -r requirements.txt
```

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests on GitHub.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements

* [pypresence](https://github.com/qwertyquerty/pypresence) for Discord Rich Presence integration
* [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap) for modern themed Tkinter widgets

---

## Contact

For support or questions, open an issue or contact me at [your.email@example.com](mailto:your.email@example.com).

If you want, I can also generate a `requirements.txt` or help you with other repo files!
```
