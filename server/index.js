const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
const multer = require('multer');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());

// 配置文件上传
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        cb(null, Date.now() + path.extname(file.originalname));
    },
});

const upload = multer({ storage });

// 连接到 MongoDB
mongoose.connect('mongodb://localhost:27017/portfolio', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => {
    console.log('Connected to MongoDB');
});

// 定义用户模型
const userSchema = new mongoose.Schema({
    username: String,
    password: String,
    nickname: String,
    isAdmin: Boolean,
});

const User = mongoose.model('User', userSchema);

// 定义作品模型
const workSchema = new mongoose.Schema({
    title: String,
    description: String,
    file: String,
    password: String,
    user: String,
});

const Work = mongoose.model('Work', workSchema);

// 定义归档模型
const archiveSchema = new mongoose.Schema({
    name: String,
    parent: { type: mongoose.Schema.Types.ObjectId, ref: 'Archive' },
});

const Archive = mongoose.model('Archive', archiveSchema);

// 定义邀请码模型
const invitationCodeSchema = new mongoose.Schema({
    code: String,
    used: Boolean,
});

const InvitationCode = mongoose.model('InvitationCode', invitationCodeSchema);

// 登录接口
app.post('/api/login', async (req, res) => {
    const { username, password } = req.body;
    try {
        const user = await User.findOne({ username, password });
        if (user) {
            res.json({ user });
        } else {
            res.status(401).json({ message: 'Invalid credentials' });
        }
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

// 注册接口
app.post('/api/register', async (req, res) => {
    const { username, password, invitationCode } = req.body;
    try {
        const validCode = await InvitationCode.findOne({
            code: invitationCode,
            used: false,
        });
        if (!validCode) {
            return res.status(400).json({ message: 'Invalid invitation code' });
        }
        const newUser = new User({ username, password, isAdmin: false });
        await newUser.save();
        validCode.used = true;
        await validCode.save();
        res.json({ message: 'Registration successful' });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

// 上传作品接口
app.post('/api/upload', upload.single('file'), async (req, res) => {
    const { title, description, password, user } = req.body;
    const file = req.file ? req.file.filename : null;
    try {
        const newWork = new Work({ title, description, file, password, user });
        await newWork.save();
        res.json({ message: 'Upload successful' });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

// 获取所有作品接口
app.get('/api/works', async (req, res) => {
    try {
        const works = await Work.find();
        res.json(works.map(work => ({
          ...work._doc,
          link: work.file? `/uploads/${work.file}` : null
        })));
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

// 创建归档接口
app.post('/api/archives', async (req, res) => {
    const { name } = req.body;
    try {
        const newArchive = new Archive({ name });
        await newArchive.save();
        res.json(newArchive);
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

// 获取所有归档接口
app.get('/api/archives', async (req, res) => {
    try {
        const archives = await Archive.find();
        res.json(archives);
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

// 更新用户信息接口
app.put('/api/users/:id', async (req, res) => {
    const { id } = req.params;
    const { nickname, password } = req.body;
    try {
        const updatedUser = await User.findByIdAndUpdate(
            id,
            { nickname, password },
            { new: true }
        );
        res.json(updatedUser);
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

// 删除用户接口
app.delete('/api/users/:id', async (req, res) => {
    const { id } = req.params;
    try {
        await User.findByIdAndDelete(id);
        res.json({ message: 'User deleted successfully' });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

// 创建邀请码接口（管理员）
app.post('/api/invitation-codes', async (req, res) => {
    const { code } = req.body;
    try {
        const newCode = new InvitationCode({ code, used: false });
        await newCode.save();
        res.json(newCode);
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

// 静态文件服务
app.use('/uploads', express.static(path.join(__dirname, '../uploads')));

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});    