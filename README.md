# Raspberry Pi Email Notifier  

<img src="https://github.com/user-attachments/assets/53349920-bfc3-475f-bda0-687abebd3f2c" alt="Project Image 1" width="400">

## Overview  

This project is an **email notification system** for **Raspberry Pi** with an **OLED SSD1331 display**.  
It displays emails on a compact screen and provides sound and LED alerts for new messages. Users can browse unread emails using buttons and a rotary encoder.  

---

## Features  

- **Live Email Preview**: Displays sender and subject on the OLED screen  
- **Unread Emails Counter**: Shows the number of unread messages  
- **Interactive Controls**: Navigate emails using buttons and a rotary encoder 
- **Notifications**:  New emails trigger sound and LED alerts

---

## Installation  

### 1. Requirements  
- Raspberry Pi (any model with GPIO support)  
- Python 3.9+  
- Configured **I2C/SPI** for the OLED SSD1331  

### 2. Clone the Repository  
```bash
git clone https://github.com/Tomek4861/RPi-Email-Notifier.git  
cd RPi-Email-Notifier  
```

### 3. Install Dependencies  
```bash
pip install simplegmail
```

### 4. Gmail API Setup  
Follow [this guide](https://github.com/jeremyephron/simplegmail) to set up **OAuth credentials** for Gmail access and input `client_secret.json` file in the root of the project directory.  

### 5. Run the Project  
```bash
python main.py
```

---

## Usage  

### Normal Mode  
- **Green Button** → Open email list  
- **Red Button** → Toggle "Do Not Disturb"  
- **Rotary Encoder** → Scroll through emails  

### Do Not Disturb Mode  
- Disables sound and LED notifications  
- New emails still appear on the OLED screen  

---

## Hardware Requirements  

| Component     | Description                     |
|--------------|---------------------------------|
| Raspberry Pi | Any model with GPIO support     |
| OLED Display | SSD1331 (96x64 px, SPI-based)   |
| Buzzer       | Active buzzer for notifications |
| Buttons      | 2x Push Buttons                 |
| Rotary Encoder | For scrolling emails         |

---

## License  
This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

---

## Authors  

- **[Tomek4861](https://github.com/Tomek4861)**
- **[tymek805](https://github.com/tymek805)**

<img src="https://github.com/user-attachments/assets/42b69907-5f14-4d58-9579-053890a53395" alt="Project Image 2" width="400">
