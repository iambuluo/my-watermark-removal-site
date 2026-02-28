"use client";

declare global {
  interface Window {
    adsbygoogle: any[];
  }
}

export default function Home() {
  if (typeof window !== "undefined") {
    window.adsbygoogle = window.adsbygoogle || [];
    try {
      window.adsbygoogle.push({});
    } catch {}
  }

  return (
    <main style={{ maxWidth: 960, margin: "0 auto", padding: 24 }}>
      <h1 style={{ fontSize: 28, fontWeight: 700 }}>批量去水印</h1>
      <p style={{ marginTop: 12 }}>
        提供免费、易用的批量去水印工具。此站点为自有品牌，无任何原项目信息。
      </p>

      <ins
        className="adsbygoogle"
        style={{ display: "block", marginTop: 24 }}
        data-ad-client="ca-pub-2259331322940741"
        data-ad-slot="1234567890"
        data-ad-format="auto"
        data-full-width-responsive="true"
      />

      <section style={{ marginTop: 24 }}>
        <h2 style={{ fontSize: 20, fontWeight: 600 }}>功能</h2>
        <ul style={{ marginTop: 8 }}>
          <li>图片批量去水印</li>
          <li>视频标识遮盖</li>
          <li>隐私信息擦除</li>
        </ul>
      </section>
    </main>
  );
}
