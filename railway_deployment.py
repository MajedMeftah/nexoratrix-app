"""
سكريبت نشر المبرمج الذكي على Railway
Railway Deployment Script for AI Programmer
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def create_railway_config():
    """إنشاء ملفات التكوين لـ Railway"""
    
    # إنشاء Procfile
    procfile_content = """web: uvicorn ai_core.web_interface:app --host 0.0.0.0 --port $PORT
worker: python ai_core/autonomous_programmer.py
"""
    
    with open("Procfile", "w") as f:
        f.write(procfile_content)
    
    # إنشاء railway.json
    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "startCommand": "uvicorn ai_core.web_interface:app --host 0.0.0.0 --port $PORT",
            "healthcheckPath": "/",
            "healthcheckTimeout": 100,
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open("railway.json", "w") as f:
        json.dump(railway_config, f, indent=2)
    
    # إنشاء nixpacks.toml
    nixpacks_content = """[phases.setup]
nixPkgs = ["python39", "pip"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["python -c 'print(\"Build completed\")'"]

[start]
cmd = "uvicorn ai_core.web_interface:app --host 0.0.0.0 --port $PORT"
"""
    
    with open("nixpacks.toml", "w") as f:
        f.write(nixpacks_content)
    
    print("✅ تم إنشاء ملفات التكوين لـ Railway")

def create_environment_file():
    """إنشاء ملف المتغيرات البيئية"""
    env_content = """# متغيرات البيئة للمبرمج الذكي
DATABASE_URL=sqlite:///./ai_knowledge.db
LOG_LEVEL=INFO
MAX_WORKERS=4
LEARNING_INTERVAL=300
IMPROVEMENT_INTERVAL=3600
GITHUB_TOKEN=your_github_token_here
OPENAI_API_KEY=your_openai_key_here
"""
    
    with open(".env.example", "w") as f:
        f.write(env_content)
    
    print("✅ تم إنشاء ملف المتغيرات البيئية")

def update_requirements():
    """تحديث ملف المتطلبات"""
    requirements = [
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.20.0",
        "sqlalchemy>=2.0.0",
        "jinja2>=3.1.0",
        "python-multipart>=0.0.6",
        "aiofiles>=23.0.0",
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
        "psutil>=5.9.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "nltk>=3.8.0",
        "textblob>=0.17.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "scikit-learn>=1.3.0",
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "datasets>=2.12.0",
        "accelerate>=0.20.0"
    ]
    
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    
    print("✅ تم تحديث ملف المتطلبات")

def create_dockerfile():
    """إنشاء Dockerfile للنشر"""
    dockerfile_content = """FROM python:3.11-slim

# تثبيت متطلبات النظام
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    git \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# إعداد مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات
COPY requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# إنشاء مجلدات ضرورية
RUN mkdir -p logs data temp

# تعيين المتغيرات البيئية
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# فتح المنفذ
EXPOSE 8000

# تشغيل التطبيق
CMD ["uvicorn", "ai_core.web_interface:app", "--host", "0.0.0.0", "--port", "8000"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print("✅ تم إنشاء Dockerfile")

def create_docker_compose():
    """إنشاء docker-compose.yml للتطوير المحلي"""
    compose_content = """version: '3.8'

services:
  ai-programmer:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - DATABASE_URL=sqlite:///./data/ai_knowledge.db
      - LOG_LEVEL=INFO
    restart: unless-stopped
    
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
"""
    
    with open("docker-compose.yml", "w") as f:
        f.write(compose_content)
    
    print("✅ تم إنشاء docker-compose.yml")

def create_deployment_script():
    """إنشاء سكريبت النشر"""
    deploy_script = """#!/bin/bash

# سكريبت نشر المبرمج الذكي على Railway

echo "🚀 بدء نشر المبرمج الذكي على Railway..."

# فحص وجود Railway CLI
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI غير مثبت. يرجى تثبيته أولاً:"
    echo "npm install -g @railway/cli"
    exit 1
fi

# تسجيل الدخول إلى Railway
echo "🔐 تسجيل الدخول إلى Railway..."
railway login

# إنشاء مشروع جديد
echo "📦 إنشاء مشروع جديد..."
railway init

# ربط المشروع
echo "🔗 ربط المشروع..."
railway link

# تعيين المتغيرات البيئية
echo "⚙️ تعيين المتغيرات البيئية..."
railway variables set DATABASE_URL=sqlite:///./ai_knowledge.db
railway variables set LOG_LEVEL=INFO
railway variables set MAX_WORKERS=4
railway variables set LEARNING_INTERVAL=300
railway variables set IMPROVEMENT_INTERVAL=3600

# نشر التطبيق
echo "🚀 نشر التطبيق..."
railway up

echo "✅ تم نشر المبرمج الذكي بنجاح!"
echo "🌐 يمكنك الوصول إليه عبر الرابط الذي سيظهر في Railway Dashboard"
"""
    
    with open("deploy.sh", "w") as f:
        f.write(deploy_script)
    
    # جعل الملف قابل للتنفيذ
    os.chmod("deploy.sh", 0o755)
    
    print("✅ تم إنشاء سكريبت النشر")

def create_readme():
    """إنشاء ملف README شامل"""
    readme_content = """# 🤖 NexoraTrix Advanced AI Programmer

## المبرمج الذكي المستقل - يبرمج، يتعلم، ويطور نفسه

### 🌟 المميزات

- **🧠 ذكاء اصطناعي متقدم**: يستخدم خوارزميات التعلم الآلي لفهم المتطلبات وتوليد أكواد عالية الجودة
- **🌐 التعلم من الإنترنت**: يبحث ويتعلم من GitHub، Stack Overflow، والمصادر التقنية
- **🔄 التطوير الذاتي**: يحلل أداءه ويحسن خوارزمياته تلقائياً
- **💻 متعدد اللغات**: يدعم جميع لغات البرمجة الشائعة
- **⚡ سرعة فائقة**: ينجز المهام البرمجية في ثوانٍ معدودة
- **🛡️ آمن وموثوق**: يختبر الأكواد المولدة ويضمن أمانها

### 🚀 التثبيت والتشغيل

#### التشغيل المحلي

```bash
# استنساخ المشروع
git clone https://github.com/your-username/nexoratrix-ai-programmer.git
cd nexoratrix-ai-programmer

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل المبرمج الذكي
python ai_core/autonomous_programmer.py

# أو تشغيل واجهة الويب
uvicorn ai_core.web_interface:app --reload
```

#### النشر على Railway

```bash
# تثبيت Railway CLI
npm install -g @railway/cli

# تشغيل سكريبت النشر
./deploy.sh
```

#### استخدام Docker

```bash
# بناء الصورة
docker build -t nexoratrix-ai .

# تشغيل الحاوية
docker run -p 8000:8000 nexoratrix-ai

# أو استخدام docker-compose
docker-compose up -d
```

### 📖 كيفية الاستخدام

#### واجهة سطر الأوامر

```python
from ai_core.autonomous_programmer import AutonomousProgrammer

# إنشاء مثيل المبرمج
programmer = AutonomousProgrammer()

# بدء النظام
await programmer.start()

# إضافة مهمة برمجية
task_id = await programmer.add_task(
    description="إنشاء API لإدارة المستخدمين",
    language="python",
    requirements=["database", "authentication", "testing"]
)

# فحص الحالة
status = await programmer.get_status()
print(status)
```

#### واجهة الويب

1. افتح المتصفح وانتقل إلى `http://localhost:8000`
2. استخدم النموذج لإضافة مهام برمجية جديدة
3. راقب التقدم من لوحة التحكم
4. اعرض النتائج والأكواد المولدة

### 🎯 القدرات

- **🌐 تطوير تطبيقات الويب**: Full-stack web applications
- **📱 تطبيقات الهاتف**: Mobile app development
- **🤖 الذكاء الاصطناعي**: ML/AI algorithms and models
- **🗄️ قواعد البيانات**: Database design and APIs
- **🎮 الألعاب**: Game development
- **📊 تحليل البيانات**: Data analysis and visualization
- **🔒 الأمان**: Security systems and encryption
- **☁️ الحوسبة السحابية**: Cloud computing solutions
- **🧪 الاختبار**: Software testing frameworks
- **⚡ تحسين الأداء**: Performance optimization

### 🔧 التكوين

#### متغيرات البيئة

```env
DATABASE_URL=sqlite:///./ai_knowledge.db
LOG_LEVEL=INFO
MAX_WORKERS=4
LEARNING_INTERVAL=300
IMPROVEMENT_INTERVAL=3600
GITHUB_TOKEN=your_github_token_here
OPENAI_API_KEY=your_openai_key_here
```

#### إعدادات متقدمة

```python
# تخصيص إعدادات التعلم
programmer.internet_learner.search_engines.update({
    "custom_source": "https://your-api.com/search"
})

# تخصيص مولد الأكواد
programmer.code_generator.supported_languages["rust"] = custom_rust_generator
```

### 📊 مراقبة الأداء

- **📈 إحصائيات الأداء**: معدل النجاح، سرعة التنفيذ
- **🧠 تتبع التعلم**: مصادر التعلم، المواضيع المكتسبة
- **💻 الأكواد المولدة**: إحصائيات الأكواد، اللغات المستخدمة
- **🔄 دورات التحسين**: تحسينات النظام، التطوير الذاتي

### 🛠️ التطوير والمساهمة

```bash
# إعداد بيئة التطوير
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\\Scripts\\activate  # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt

# تشغيل الاختبارات
pytest tests/

# فحص جودة الكود
flake8 ai_core/
black ai_core/
mypy ai_core/
```

### 📝 API Documentation

#### إضافة مهمة

```http
POST /add-task
Content-Type: application/x-www-form-urlencoded

description=إنشاء API لإدارة المستخدمين&language=python&requirements=database,api,testing
```

#### فحص الحالة

```http
GET /api/status
```

#### تشغيل التعلم

```http
POST /api/learn
Content-Type: application/x-www-form-urlencoded

topic=advanced python programming
```

### 🔮 الخطط المستقبلية

- **🎨 واجهة مستخدم محسنة**: React/Vue.js frontend
- **🔌 نظام الإضافات**: Plugin system for extensions
- **🌍 دعم لغات متعددة**: Multi-language UI support
- **📱 تطبيق محمول**: Mobile app for task management
- **🤝 التعاون الجماعي**: Team collaboration features
- **🎯 تخصص المجالات**: Domain-specific programming assistants

### 📞 الدعم والمساعدة

- **📧 البريد الإلكتروني**: support@nexoratrix.com
- **💬 Discord**: [رابط الخادم]
- **📖 الوثائق**: [رابط الوثائق]
- **🐛 الإبلاغ عن الأخطاء**: [GitHub Issues]

### 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT. راجع ملف [LICENSE](LICENSE) للتفاصيل.

### 🙏 شكر وتقدير

- OpenAI لنماذج GPT
- Hugging Face لمكتبة Transformers
- FastAPI لإطار العمل السريع
- Railway لمنصة النشر السحابية

---

**🤖 NexoraTrix - حيث يلتقي الذكاء الاصطناعي بالإبداع البرمجي**
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ تم إنشاء ملف README")

def main():
    """الوظيفة الرئيسية لإعداد المشروع للنشر"""
    print("🚀 إعداد مشروع المبرمج الذكي للنشر على Railway")
    print("=" * 60)
    
    # إنشاء المجلدات الضرورية
    os.makedirs("ai_core", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("temp", exist_ok=True)
    
    # إنشاء الملفات
    create_railway_config()
    create_environment_file()
    update_requirements()
    create_dockerfile()
    create_docker_compose()
    create_deployment_script()
    create_readme()
    
    print("\n✅ تم إعداد المشروع بنجاح!")
    print("\n📋 الخطوات التالية:")
    print("1. راجع ملف .env.example وأضف المتغيرات المطلوبة")
    print("2. تأكد من تثبيت Railway CLI: npm install -g @railway/cli")
    print("3. شغل سكريبت النشر: ./deploy.sh")
    print("4. أو استخدم Docker: docker-compose up -d")
    print("\n🌐 بعد النشر، ستحصل على رابط للوصول إلى المبرمج الذكي")

if __name__ == "__main__":
    main()