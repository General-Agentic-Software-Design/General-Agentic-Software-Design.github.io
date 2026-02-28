class BlogEngine {
    constructor() {
        this.contentArea = document.getElementById('content');
        this.loader = document.getElementById('loader');
        this.headerTitle = document.getElementById('header-title');
        this.headerSubtitle = document.getElementById('header-subtitle');
        this.siteHeader = document.getElementById('site-header');

        this.blogs = [];
        this.defaultTitle = 'General Agentic Software Design';
        this.defaultSubtitle = 'Architecting the future of AI-driven engineering.';

        // Make logo/title clickable
        this.siteHeader.style.cursor = 'pointer';
        this.siteHeader.onclick = () => window.location.hash = '';

        window.addEventListener('hashchange', () => this.handleRouting());
    }

    async init() {
        try {
            const response = await fetch('blogs/blogs.json');
            const data = await response.json();
            this.blogs = data.blogs;
            await this.handleRouting();
        } catch (error) {
            console.error('Failed to load blogs manifest:', error);
            this.contentArea.innerHTML = '<div class="error">Failed to load blog index. Please try again later.</div>';
        }
    }

    showLoader(show) {
        this.loader.style.display = show ? 'block' : 'none';
        if (show) this.contentArea.style.opacity = '0.5';
        else this.contentArea.style.opacity = '1';
    }

    async handleRouting() {
        const hash = window.location.hash.slice(1);
        if (!hash) {
            this.renderHome();
            return;
        }

        const [blogId, partId] = hash.split('/');
        if (blogId && partId) {
            await this.renderPart(blogId, partId);
        } else {
            this.renderHome();
        }
    }

    renderHome() {
        document.title = this.defaultTitle;
        this.headerTitle.innerText = this.defaultTitle;
        this.headerSubtitle.innerText = this.defaultSubtitle;

        let html = '';
        this.blogs.forEach(blog => {
            html += `
                <div class="series-group">
                    <h2 class="series-heading">${blog.title}</h2>
                    <ul class="parts-list">
            `;

            blog.parts.forEach(part => {
                html += `
                    <li>
                        <a href="#${blog.id}/${part.id}" class="blog-link ${part.id === 'intro' ? 'intro-link' : ''}">
                            <span class="blog-title">${part.title}</span>
                            <span class="blog-meta">${part.description}</span>
                        </a>
                    </li>
                `;
            });

            html += `
                    </ul>
                </div>
            `;
        });

        this.contentArea.innerHTML = html;
        window.scrollTo(0, 0);
    }

    async renderPart(blogId, partId) {
        const blog = this.blogs.find(b => b.id === blogId);
        if (!blog) return this.renderHome();

        const partIndex = blog.parts.findIndex(p => p.id === partId);
        const part = blog.parts[partIndex];
        if (!part) return this.renderHome();

        this.showLoader(true);
        try {
            const response = await fetch(part.file);
            const md = await response.text();

            const rawHtml = marked.parse(md);
            const cleanHtml = DOMPurify.sanitize(rawHtml);

            document.title = `${part.title} | ${blog.title}`;
            this.headerTitle.innerText = blog.title;
            this.headerSubtitle.innerText = part.title;

            const prevPart = blog.parts[partIndex - 1];
            const nextPart = blog.parts[partIndex + 1];

            let navHtml = `
                <nav class="breadcrumb">
                    <a href="#">Home</a> <span>/</span> ${blog.title}
                </nav>
                <article class="content">
                    ${cleanHtml}
                </article>
                <div class="navigation-links">
                    ${prevPart ? `<a href="#${blog.id}/${prevPart.id}">← ${prevPart.title}</a>` : '<span></span>'}
                    ${nextPart ? `<a href="#${blog.id}/${nextPart.id}">${nextPart.title} →</a>` : '<span></span>'}
                </div>
            `;

            this.contentArea.innerHTML = navHtml;
            this.rewriteLinks(blogId);
            window.scrollTo(0, 0);
        } catch (error) {
            console.error('Failed to load blog part:', error);
            this.contentArea.innerHTML = '<div class="error">Failed to load the blog post. It might have been moved or deleted.</div>';
        } finally {
            this.showLoader(false);
        }
    }

    rewriteLinks(blogId) {
        const links = this.contentArea.querySelectorAll('a');
        links.forEach(link => {
            const href = link.getAttribute('href');
            if (href && (href.startsWith('./') || !href.includes('://'))) {
                // Potential internal link
                if (href.endsWith('.md') || href.endsWith('.html')) {
                    const parts = href.split('/');
                    const filename = parts[parts.length - 1];
                    const id = filename.replace('.md', '').replace('.html', '').toLowerCase();

                    // Standardize intro
                    const finalId = id === 'intro' ? 'intro' : id;
                    link.setAttribute('href', `#${blogId}/${finalId}`);
                }
            }
        });
    }
}

const engine = new BlogEngine();
engine.init();
