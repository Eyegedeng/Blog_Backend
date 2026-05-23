// ===== 状态 =====
let token = localStorage.getItem("token") || null;

// ===== DOM 元素 =====
const navEl = document.getElementById("nav");
const appEl = document.getElementById("app");

// 弹窗
const modalOverlay = document.getElementById("modal-overlay");
const modalTitle = document.getElementById("modal-title");
const modalBody = document.getElementById("modal-body");
const modalFooter = document.getElementById("modal-footer");

// ===== 入口 =====
render();

// ===== 渲染函数 =====
function render() {
    renderNav();
    renderPosts();
}

function renderNav() {
    if (token) {
        navEl.innerHTML = `
            <button class="btn btn-primary" onclick="showCreateModal()">写文章</button>
            <button class="btn-logout" onclick="logout()">退出登录</button>
        `;
    } else {
        navEl.innerHTML = `
            <button onclick="showLoginModal()">登录</button>
            <button class="btn btn-primary" onclick="showRegisterModal()">注册</button>
        `;
    }
}

async function renderPosts() {
    try {
        const res = await fetch("/posts");
        const posts = await res.json();

        if (posts.length === 0) {
            appEl.innerHTML = '<div class="empty-state">还没有文章</div>';
            return;
        }

        appEl.innerHTML = posts
            .map((post) => {
                const canEdit = token
                    ? `<button class="btn btn-edit" onclick="showEditModal(${post.id}, '${escapeAttr(post.title)}', '${escapeAttr(post.content)}')">编辑</button>
                       <button class="btn btn-danger" onclick="deletePost(${post.id})">删除</button>`
                    : "";
                return `
                    <div class="post-card">
                        <h2>${escapeHtml(post.title)}</h2>
                        <p>${escapeHtml(post.content)}</p>
                        <div class="meta">作者：${escapeHtml(post.author_name)}</div>
                        ${canEdit}
                    </div>
                `;
            })
            .join("");
    } catch (e) {
        appEl.innerHTML = '<div class="empty-state">加载失败</div>';
    }
}

// ===== 认证 =====
async function register() {
    const username = document.getElementById("reg-username").value;
    const password = document.getElementById("reg-password").value;
    const errEl = document.getElementById("reg-error");

    try {
        const res = await fetch("/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });
        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.detail);
        }
        closeModal();
        showLoginModal();
    } catch (e) {
        errEl.textContent = e.message;
        errEl.style.display = "block";
    }
}

async function login() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    const errEl = document.getElementById("login-error");

    // OAuth2 表单格式，不是 JSON
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const res = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData,
        });
        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.detail);
        }
        const data = await res.json();
        token = data.access_token;
        localStorage.setItem("token", token);
        closeModal();
        render();
    } catch (e) {
        errEl.textContent = e.message;
        errEl.style.display = "block";
    }
}

function logout() {
    token = null;
    localStorage.removeItem("token");
    render();
}

// ===== 文章 CRUD =====
async function createPost() {
    const title = document.getElementById("post-title").value;
    const content = document.getElementById("post-content").value;
    const errEl = document.getElementById("post-error");

    try {
        const res = await fetch("/posts", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ title, content }),
        });
        if (!res.ok) throw new Error((await res.json()).detail);
        closeModal();
        render();
    } catch (e) {
        errEl.textContent = e.message;
        errEl.style.display = "block";
    }
}

async function updatePost(postId) {
    const title = document.getElementById("post-title").value;
    const content = document.getElementById("post-content").value;
    const errEl = document.getElementById("post-error");

    try {
        const res = await fetch(`/posts/${postId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({ title, content }),
        });
        if (!res.ok) throw new Error((await res.json()).detail);
        closeModal();
        render();
    } catch (e) {
        errEl.textContent = e.message;
        errEl.style.display = "block";
    }
}

async function deletePost(postId) {
    if (!confirm("确定删除这篇文章？")) return;
    const res = await fetch(`/posts/${postId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) {
        const data = await res.json();
        alert(data.detail);
        return;
    }
    render();
}

// ===== 弹窗 =====
function showLoginModal() {
    modalTitle.textContent = "登录";
    modalBody.innerHTML = `
        <div class="error-msg" id="login-error"></div>
        <div class="form-group">
            <label>用户名</label>
            <input id="login-username" type="text" placeholder="请输入用户名">
        </div>
        <div class="form-group">
            <label>密码</label>
            <input id="login-password" type="password" placeholder="请输入密码">
        </div>
    `;
    modalFooter.innerHTML = `
        <button class="btn btn-cancel" onclick="closeModal()">取消</button>
        <button class="btn btn-primary" onclick="login()">登录</button>
    `;
    modalOverlay.classList.add("active");
}

function showRegisterModal() {
    modalTitle.textContent = "注册";
    modalBody.innerHTML = `
        <div class="error-msg" id="reg-error"></div>
        <div class="form-group">
            <label>用户名</label>
            <input id="reg-username" type="text" placeholder="请输入用户名">
        </div>
        <div class="form-group">
            <label>密码</label>
            <input id="reg-password" type="password" placeholder="请输入密码">
        </div>
    `;
    modalFooter.innerHTML = `
        <button class="btn btn-cancel" onclick="closeModal()">取消</button>
        <button class="btn btn-primary" onclick="register()">注册</button>
    `;
    modalOverlay.classList.add("active");
}

function showCreateModal() {
    modalTitle.textContent = "写文章";
    modalBody.innerHTML = `
        <div class="error-msg" id="post-error"></div>
        <div class="form-group">
            <label>标题</label>
            <input id="post-title" type="text" placeholder="请输入标题">
        </div>
        <div class="form-group">
            <label>内容</label>
            <textarea id="post-content" placeholder="请输入内容"></textarea>
        </div>
    `;
    modalFooter.innerHTML = `
        <button class="btn btn-cancel" onclick="closeModal()">取消</button>
        <button class="btn btn-primary" onclick="createPost()">发布</button>
    `;
    modalOverlay.classList.add("active");
}

function showEditModal(postId, title, content) {
    modalTitle.textContent = "编辑文章";
    modalBody.innerHTML = `
        <div class="error-msg" id="post-error"></div>
        <div class="form-group">
            <label>标题</label>
            <input id="post-title" type="text" value="${title}">
        </div>
        <div class="form-group">
            <label>内容</label>
            <textarea id="post-content">${content}</textarea>
        </div>
    `;
    modalFooter.innerHTML = `
        <button class="btn btn-cancel" onclick="closeModal()">取消</button>
        <button class="btn btn-primary" onclick="updatePost(${postId})">保存</button>
    `;
    modalOverlay.classList.add("active");
}

function closeModal() {
    modalOverlay.classList.remove("active");
}

// 点击遮罩关闭
modalOverlay.addEventListener("click", function (e) {
    if (e.target === modalOverlay) closeModal();
});

// ===== 工具函数 =====
function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

function escapeAttr(str) {
    // HTML 属性转义：除了 <>&" 还要转义单引号，否则 onclick='...' 会断
    return escapeHtml(str).replace(/'/g, "&#39;");
}
