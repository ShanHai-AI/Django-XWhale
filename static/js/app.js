/*
 * @Author: LiQiang
 * @Date: 2025-04-09 20:51:12
 * @LastEditors: LiQiang
 * @LastEditTime: 2025-04-10 15:34:26
 * @Description: 文件描述
 */
// app.js

const alertMessagesDiv = document.getElementById('alert-messages');
const emotionAlertMessagesDiv = document.getElementById('emotion-alert-messages');
const modal = document.getElementById('media-modal');
const modalImagePreview = document.getElementById('modal-image-preview');
const modalVideoPreview = document.getElementById('modal-video-preview');

// 获取关闭按钮
//const closeModalButton = document.getElementById('close-modal-button');

// 左侧预警消息 WebSocket
const alertWebSocket = new WebSocket('ws://127.0.0.1:16532/alerts');

// 监听预警消息连接状态
alertWebSocket.onopen = () => {
    console.log('预警消息 WebSocket 连接已建立');
};

// 右侧视频流 WebSocket
const videoWebSocket = new WebSocket('ws://127.0.0.1:16532/video_feed');

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
    // 行为预警信息
    const alertMessagesDiv = document.getElementById('alert-messages');
    //心理预警信息
    const emotionAlertMessagesDiv = document.getElementById('emotion-alert-messages');

    // 创建一个新的消息元素
    const messageElement = document.createElement('li');
    const messageElementAlerts = document.createElement('li');
    messageElement.className = 'fl';
    messageElementAlerts.className= 'fl';

    // 构造消息内容
    const timestamp = new Date(message.timestamp).toLocaleTimeString();
    const content = message.alert || '未知消息';
    const description = message.description || '无描述信息';
    const type=message.type || '未知类型';

    // 设置消息内容
    messageElement.innerHTML = `
        <p><strong>时间:</strong> ${timestamp}</p>
        <p><strong>预警信息:</strong> ${content}</p>
    `;
    messageElementAlerts.innerHTML = `
        <p><strong>时间:</strong> ${timestamp}</p>
        <p><strong>预警信息:</strong> ${content}</p>
        <p style="color:#FF4500;"><strong>方案:</strong>已发送短信到亲友手机和紧急救护人员</p>
    `;
    // 创建按钮容器
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'button-container';
    
    // 添加视频文件链接（如果有）
    // 添加视频文件链接（如果有）
    if (message.video_file_name) {
        const videoButton = document.createElement('button');
        videoButton.textContent = `点击查看视频`;
        videoButton.classList.add('green-button');
        // videoLink.textContent = `点击查看视频: ${message.video_file_name}`;
        videoButton.onclick = () => openMediaModal('http://127.0.0.1:8000/media/video_warning/' + message.video_file_name, 'video');
//        messageElement.appendChild(document.createElement('br'));
        buttonContainer.appendChild(videoButton);
    }

    // 添加图片文件链接（如果有）
    if (message.picture_file_name) {
        const pictureButton = document.createElement('button');
        pictureButton.textContent = `点击查看图片`;
        pictureButton.classList.add('blue-button');
        pictureButton.onclick = () => openMediaModal('http://127.0.0.1:8000/media/image_warning/' + message.picture_file_name, 'image');
//        messageElement.appendChild(document.createElement('br'));
        buttonContainer.appendChild(pictureButton);
    }
    // 将按钮容器添加到消息元素
    messageElement.appendChild(buttonContainer);
    messageElementAlerts.appendChild(buttonContainer);
    // 将消息元素插入到列表的顶部

//    const messageElementForAlerts = messageElement.cloneNode(true); // 克隆消息元素
//    alertMessagesDiv.prepend(messageElementForAlerts);

//    const messageElementForEmotion = messageElement.cloneNode(true); // 再次克隆
//    emotionAlertMessagesDiv.prepend(messageElementForEmotion);
    if (type=='行为异常'){
    alertMessagesDiv.prepend(messageElementAlerts); // 使用 prepend 方法
    }
    if (type=='无异常'){
    emotionAlertMessagesDiv.prepend(messageElement);} // 使用 prepend 方法
//    }else{
//    alertMessagesDiv.prepend(messageElement); // 使用 prepend 方法
//    emotionAlertMessagesDiv.prepend(messageElement); // 使用 prepend 方法

//    // 将消息元素添加到页面
//    alertMessagesDiv.appendChild(messageElement);

    // 滚动到底部
//    alertMessagesDiv.scrollTop = alertMessagesDiv.scrollHeight;
// 如果需要限制最大消息数量，可以删除多余的旧消息
    const maxMessages = 50; // 最大消息数量
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

    // 隐藏所有媒体内容
    modalImagePreview.style.display = 'none';
    modalVideoPreview.style.display = 'none';

    if (type === 'image') {
        // 显示图片
        modalImagePreview.src = url;
        modalImagePreview.style.display = 'block';
    } else if (type === 'video') {
        // 显示视频
        modalVideoPreview.src = url;
        modalVideoPreview.style.display = 'block';
    }

    // 显示弹窗
    modal.style.display = 'block';
}
// const closeModalButton = document.querySelector('.close');
const closeModalButton = document.getElementById('close-modal-button');
// 关闭弹窗
closeModalButton.onclick = (event) => {
    modal.style.display = 'none';
    modalImagePreview.src = ''; // 清空图片源
    modalVideoPreview.src = ''; // 清空视频源
};

// 点击弹窗外的区域关闭弹窗
window.onclick = (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
        modalImagePreview.src = ''; // 清空图片源
        modalVideoPreview.src = ''; // 清空视频源
    }
};

