// app.js

const AppConfig = {
    ALERT_WS_URL: 'ws://192.168.3.6:16532/alerts',
    VIDEO_WS_URL: 'ws://192.168.3.6:16532/video_feed',
    MEDIA_BASE_URL: 'http://127.0.0.1:8000/media'
};

const alertMessagesDiv = document.getElementById('alert-messages');
const emotionAlertMessagesDiv = document.getElementById('emotion-alert-messages');
const modal = document.getElementById('media-modal');
const modalImagePreview = document.getElementById('modal-image-preview');
const modalVideoPreview = document.getElementById('modal-video-preview');

// 左侧预警消息 WebSocket
const alertWebSocket = new WebSocket(AppConfig.ALERT_WS_URL);

// 监听预警消息连接状态
alertWebSocket.onopen = () => {
    console.log('预警消息 WebSocket 连接已建立');
};

// 右侧视频流 WebSocket
const videoWebSocket = new WebSocket(AppConfig.VIDEO_WS_URL);

// 监听视频流连接状态
videoWebSocket.onopen = () => {
    console.log('视频流 WebSocket 连接已建立');
};

// 接收视频流数据
videoWebSocket.onmessage = (event) => {
    const videoFeed = document.getElementById('video-feed');
    try {
        // 将二进制数据转换为 Blob URL
        const blob = new Blob([event.data], { type: 'image/jpeg' });
        const url = URL.createObjectURL(blob);
        videoFeed.src = url;

        // 释放旧的 Blob URL（避免内存泄漏）
        if (videoFeed.dataset.lastBlobUrl) {
            URL.revokeObjectURL(videoFeed.dataset.lastBlobUrl);
        }
        videoFeed.dataset.lastBlobUrl = url;
    } catch (error) {
        console.error('解析视频流失败:', error);
    }
};

// 接收预警消息
alertWebSocket.onmessage = (event) => {
    try {
        const message = JSON.parse(event.data);
        console.log('收到预警消息:', message);
        displayAlertMessage(message);
    } catch (error) {
        console.error('解析消息失败:', error);
        console.error('原始消息内容:', event.data);
    }
};

function displayAlertMessage(message) {
    const alertMessagesDiv = document.getElementById('alert-messages');
    const emotionAlertMessagesDiv = document.getElementById('emotion-alert-messages');

    const messageElement = document.createElement('li');
    const messageElementAlerts = document.createElement('li');
    messageElement.className = 'fl';
    messageElementAlerts.className = 'fl';

    const timestamp = new Date(message.timestamp).toLocaleTimeString();
    const content = message.alert || '未知消息';
    const description = message.description || '无描述信息';
    const type = message.type || '未知类型';

    messageElement.innerHTML = `
        <p><strong>时间:</strong> ${timestamp}</p>
        <p><strong>预警信息:</strong> ${content}</p>
    `;
    messageElementAlerts.innerHTML = `
        <p><strong>时间:</strong> ${timestamp}</p>
        <p><strong>预警信息:</strong> ${content}</p>
        <p style="color:#FF4500;"><strong>方案:</strong>已发送短信到亲友手机和紧急救护人员</p>
    `;

    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'button-container';

    if (message.video_file_name) {
        const videoButton = document.createElement('button');
        videoButton.textContent = `点击查看视频`;
        videoButton.classList.add('green-button');
        videoButton.onclick = () => openMediaModal(`${AppConfig.MEDIA_BASE_URL}/video_warning/${message.video_file_name}`, 'video');
        buttonContainer.appendChild(videoButton);
    }

    if (message.picture_file_name) {
        const pictureButton = document.createElement('button');
        pictureButton.textContent = `点击查看图片`;
        pictureButton.classList.add('blue-button');
        pictureButton.onclick = () => openMediaModal(`${AppConfig.MEDIA_BASE_URL}/image_warning/${message.picture_file_name}`, 'image');
        buttonContainer.appendChild(pictureButton);
    }

    messageElement.appendChild(buttonContainer);
    messageElementAlerts.appendChild(buttonContainer);

    if (type === '行为异常') {
        alertMessagesDiv.prepend(messageElementAlerts);
    } else if (type === '无异常') {
        emotionAlertMessagesDiv.prepend(messageElement);
    }

    // 控制最大消息数量
    const maxMessages = 50;
    while (alertMessagesDiv.children.length > maxMessages) {
        alertMessagesDiv.removeChild(alertMessagesDiv.lastElementChild);
    }
    while (emotionAlertMessagesDiv.children.length > maxMessages) {
        emotionAlertMessagesDiv.removeChild(emotionAlertMessagesDiv.lastElementChild);
    }
}

/**
 * 打开媒体弹窗
 * @param {string} url - 媒体文件的 URL
 * @param {string} type - 媒体类型 ('image' 或 'video')
 */
function openMediaModal(url, type) {
    const modalImagePreview = document.getElementById('image-preview');
    const modalVideoPreview = document.getElementById('video-preview');
    const modal = document.getElementById('media-modal');

    modalImagePreview.style.display = 'none';
    modalVideoPreview.style.display = 'none';

    if (type === 'image') {
        modalImagePreview.src = url;
        modalImagePreview.style.display = 'block';
    } else if (type === 'video') {
        modalVideoPreview.src = url;
        modalVideoPreview.style.display = 'block';
    }

    modal.style.display = 'block';
}

// 关闭弹窗按钮
const closeModalButton = document.getElementById('close-modal-button');
closeModalButton.onclick = (event) => {
    modal.style.display = 'none';
    modalImagePreview.src = '';
    modalVideoPreview.src = '';
};

// 点击弹窗外区域关闭
window.onclick = (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
        modalImagePreview.src = '';
        modalVideoPreview.src = '';
    }
};