export async function onTurnstileSuccess (token) {
    let submitto = window.submitto;
    console.log(submitto)
    try {
        const response = await fetch(submitto, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": window.csrf_token
            },
            body: JSON.stringify({
                token: token
            }),
        });
        const result = await response.json();
        
        if (result.success) {
            const popup = document.querySelector('.pop-up');
            const showid = document.getElementById('id_result');
            const showreason = document.getElementById('reason');
            const tips = document.getElementById('tips');
            window.id = result.id;
            tips.innerHTML = "验证码仅限单次有效";
            showid.innerHTML = result.id;
            showreason.innerHTML = result.reason;
            popup.style.backgroundColor = `rgb(82, 196, 26)`;
            popup.style.display = "flex";
        } else {
            const popup = document.querySelector('.pop-up');
            const showreason = document.getElementById('reason');
            showreason.innerHTML = result.reason;
            popup.style.backgroundColor = `rgb(255, 77, 79)`;
            popup.style.display = "flex";
        }
    } catch (error) {
        console.error("请求失败:", error);
    }
}

async function onButtonPress () {
    try {
        await navigator.clipboard.writeText(window.id);
        const popup = document.querySelector('.pop-up');
        popup.style.display = "none";
    } catch (err) {
        console.error('无法复制:', err);
    }
}