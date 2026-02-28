# 批量去水印网站

- 技术栈：Next.js 14 + React 18
- 广告：已集成 Google AdSense（请替换 client 与 slot）
- 部署：推荐使用 Vercel，一键导入 Git 仓库

## 使用

1. 进入 `web` 目录执行 `npm install`
2. 本地开发：`npm run dev`
3. 构建：`npm run build`
4. 部署到 Vercel：新建项目并选择 `web` 目录作为根目录

## 配置

- 在 `app/layout.tsx` 与 `app/page.tsx` 中将 `ca-pub-0000000000000000` 与 `data-ad-slot="1234567890"` 替换为你的 AdSense 信息
- 如需自定义品牌文案，修改 `metadata` 与首页文案
