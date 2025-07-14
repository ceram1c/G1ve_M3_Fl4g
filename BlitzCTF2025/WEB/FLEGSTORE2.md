*FLEGSTORE2*
<img width="2879" height="1652" alt="image" src="https://github.com/user-attachments/assets/fa22ec5e-c1a9-4953-a031-40eee99e6c97" />
Bài yêu cầu ta click với thời gian cooldown, 1 click = 1 điểm, cho đến khi đạt 9999 điểm. Và cũng phải save mỗi 5 lần click để đề phòng bot.
INSPECT HTML ta thấy luôn cả script của web
```
<script>
    let clickCount = 5;
    let originalClicks = 5;
    let lastClickTime = 0;

    const clickCountEl = document.getElementById('clickCount');
    const toast = document.getElementById('toast');
    const settingsPanel = document.getElementById('settingsPanel');
    const overlay = document.getElementById('overlay');
    const settingsButton = document.getElementById('settingsButton');
    const closeSettings = document.getElementById('closeSettings');

    function updateClickCount() {
      clickCountEl.textContent = clickCount;
    }

    function showToast(message) {
      toast.textContent = message;
      toast.classList.add('show');
      setTimeout(() => toast.classList.remove('show'), 3000);
    }

    function toggleSettings() {
      settingsPanel.classList.toggle('open');
      overlay.classList.toggle('active');
    }

    settingsButton.addEventListener('click', toggleSettings);
    closeSettings.addEventListener('click', toggleSettings);
    overlay.addEventListener('click', toggleSettings);

    document.getElementById('clickButton').addEventListener('click', () => {
      const now = Date.now();
      const cooldown = 1000;

      if (now - lastClickTime >= cooldown) {
        clickCount++;
        updateClickCount();
        lastClickTime = now;

        clickCountEl.style.transform = 'scale(1.05)';
        setTimeout(() => clickCountEl.style.transform = 'scale(1)', 100);

        if (clickCount - originalClicks > 5) {
          showToast("Reminder: Save your progress now.");
        }

        startCooldown(cooldown);
      }
    });

    function startCooldown(duration) {
      const progressBar = document.getElementById('cooldownProgress');
      let elapsed = 0;
      const interval = setInterval(() => {
        elapsed += 10;
        const percent = Math.min((elapsed / duration) * 100, 100);
        progressBar.value = percent;
        if (elapsed >= duration) {
          clearInterval(interval);
          progressBar.value = 0;
        }
      }, 10);
    }

    document.getElementById('saveButton').addEventListener('click', () => {
      fetch('/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ clicks: clickCount })
      })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          showToast(data.error);
        } else {
          showToast(data.message);
          originalClicks = clickCount;
        }
      })
      .catch(() => showToast("Error saving."));
    });

    document.getElementById('createBackup').addEventListener('click', () => {
      showToast("Creating backup...");

      fetch('/create_backup', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
          const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
          const link = document.createElement('a');
          link.href = URL.createObjectURL(blob);
          link.download = 'backup.json';
          link.click();

          showToast("Backup created!");
        })
        .catch(() => showToast("Error creating backup"));

      toggleSettings();
    });


document.getElementById('restoreBackup').addEventListener('click', () => {
  // Create an input element to allow the user to select a file
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.json';  // Only accept .json files

  input.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (!file) {
      showToast("No file selected.");
      return;
    }

    // Create a FileReader to read the contents of the selected file
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const jsonData = JSON.parse(reader.result);

        // Sending the JSON data to the backend via POST request
        fetch('/restore_backup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(jsonData),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast("Backup restored successfully!");
                setTimeout(() => {
                    window.location.href = '/';  // Redirect to the home page
                }, 1000);  // 1 second delay
          } else {
            showToast(data.error || "Error restoring backup.");
          }
        })
        .catch(() => showToast("Error sending backup data."));
      } catch (error) {
        showToast("Error reading backup file.");
      }
    };

    reader.readAsText(file);
  });

  input.click();  // Trigger the file input dialog
});


    document.getElementById('getFlag').addEventListener('click', () => {
        window.location.href = '/buy';
    });

    updateClickCount();
  </script>
  ```

Trong đoạn code trên, ta thấy được 2 function create backup and restore backup. Phần restore backup sẽ khôi phục dữ liệu trong file mà ko qua kiểm tra nào. Vậy ta chỉ cần sửa được file backup bằng với số điểm ta cần
Tải file backup về thì ta có 1 file json:
```
{
  "profile": {
    "user": {
      "id": "user_78291",
      "username": "PlayerOne",
      "email": "playerone@example.com",
      "join_date": "2021-03-12T14:55:02Z",
      "last_login": "2025-04-22T09:15:33Z"
    },
    "settings": {
      "theme": "dark",
      "language": "en",
      "notifications_enabled": true,
      "privacy_level": "high"
    }
  },
  "game": {
    "title": "ChronoTapper",
    "version": "v1.9.2-beta",
    "developer": "Shadowh",
    "build_hash": "b9248f67a21eaa6e82647e441af7204f9b40a9ad",
    "content_hash": "a31d7c8ff60da6873fca63764ad432cfed0f8a7c",
    "session_id": "137cd852f184a187788ee3225c30c6e1"
  },
  "stats": {
    "level": 15,
    "progress": 78,
    "quests_completed": 3,
    "achievements": [
      "fast_clicker",
      "precision_tapper"
    ],
    "items_purchased": [
      "premium_pack",
      "double_points_boost"
    ]
  },
  "session_data": {
    "timestamp": "2025-07-11T12:29:07.465108",
    "clicks_data": {
      "clickStore": 0,
      "currency": "tokens",
      "daily_limit_reached": false
    },
    "last_session_duration": "30m 25s",
    "current_session_duration": "5m 17s",
    "active_boosts": [
      "speed_boost",
      "click_multiplier"
    ],
    "server_id": "srv_2098b",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "client_version": "v1.9.2-beta"
  },
  "security": {
    "session_token": "137cd852f184a187788ee3225c30c6e1",
    "csrf_token": "fa482af91aa12339d8faa881b6afebcf65927b0cdeb8fc6d7a1a7d797b442d1b",
    "integrity_check": "a160ff8efa29403fa5bf55e6c36bc1a36bc851e0d73ae3f284091f79cf4b7a463087bc1d498c8d5b7043475d626ee528342901f19142ed42290bbe1b77b4475c",
    "previous_backup_hash": "3b9e69a6beae74069f74d3b2f94668d4a0249d1f"
  },
  "metadata": {
    "device_id": "d3d6f12b-545f-40b6-a920-76734667b758",
    "region": "US-EAST-2",
    "os": "Windows 10",
    "browser": "Chrome 92.0.4515.159",
    "network": "fiber"
  }
}
```
Ở đây trường ta quan tâm liên quan đến session data có hiện thị số clickcount -> sửa nó thành 9999 -> restore backup
<img width="1822" height="1316" alt="image" src="https://github.com/user-attachments/assets/88af083e-6567-43ac-ae1c-c3437988d2b2" />
Blitz{FlEg_l00t3R_sh0p_Butt_w1th_cl1qu35}



