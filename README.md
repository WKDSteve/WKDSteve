# Who I Am and What I Do

<p align="justify">
Hi, I'm glad you're here! Based in Vienna, I mainly focus on CLI-Tools, Neovim, Web Development & Cyber Security. I enjoy experimenting with languages like ZIG, Go, and sometimes Rust, and I also dive into "close to the hardware" topics.

I look forward to any kind of exchange. Feel free to reach out and we can chat on Discord about the wonderful world of information technology!  

**One important note:**  
Access to technology should be a given for everyone, but unfortunately it is not. It is unevenly distributed and, despite its central importance, still not freely accessible. Our data is being collected daily, often without our knowledge or consent, raising critical concerns about privacy and security.
</p>

<p>We must advocate for transparency and control over how our information is used!</p>

[Netzpolitik.org](https://netzpolitik.org) – get organized!

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=StefanBartl&theme=tokyonight&border_color=333&layout=donut&hide_title=true">
</p>

> “A primary goal of any engineer should be to continually be learning and understanding.”  
> — John Carmack

> “Programs must be written for people to read, and only incidentally for machines to execute.”  
> — Harold Abelson

## Projects for You

- [**nvim-replacer**](https://github.com/StefanBartl/replacer)  
  Project-wide search-and-replace with ripgrep, an interactive picker (fzf-lua or Telescope), live preview, and precise application of changes.

- [**reposcope.nvim**](https://github.com/StefanBartl/reposcope.nvim)  
  Search, preview, and clone GitHub repositories directly from inside Neovim. Modular, minimal, Telescope-inspired interface.

- [**nvim-cmdlog**](https://github.com/StefanBartl/nvim-cmdlog)  
  A lightweight, modern Neovim plugin to interactively view, search, and reuse command-line mode (`:`) history and shell history using Telescope or fzf.

- [**telescope-selected-index**](https://github.com/StefanBartl/telescope-selected-index)  
  A lightweight Telescope.nvim plugin to show the index of the currently selected entry in the results window. Designed for easy integration.

## Infos

```ts
/** 
 * Type-safe self-description
 */
type Mood = "focused" | "curious" | "shipping";

interface CodingProfile {
  hoursSpentCodingLastMonth?: number;
  favoriteEditor?: "nvim" | "vim" | "vscode";
  languageNotes: ReadonlyMap<string, string>;
  toolchainCount: number;
  yearsOfExperience: number;
  securityTools: ReadonlyArray<string>;
  certificates?: ReadonlyArray<string>;
  currentlyLearning?: ReadonlyArray<string>;
  nickname: string;
  contact: string;
  mood: Mood;
  getMood: () => string;
}

const profile: CodingProfile = {
  nickname: "lavalue",
  contact: "l.value.impl@gmail.com",
  mood: "focused",
  getMood: () => "focused on deep work and delivery",
  hoursSpentCodingLastMonth: 130,
  favoriteEditor: "nvim",
  languageNotes: new Map<string, string>([
    ["lua", "Primary for Neovim plugins and fast scripting."],
    ["typescript", "Comfortable for modern web tooling and type-safety."],
    ["c++", "Enjoys performance and control when needed."],
    ["go", "Pragmatic choice for tooling and backends."],
    ["lisp", "Great for learning and meta-programming ideas."],
    ["rust", "Valuable for systems work, still exploring."]
  ]),
  toolchainCount: 14,
  yearsOfExperience: 4,
  securityTools: ["Wireshark", "HackRF One", "Metasploit", "firmware tools"],
  certificates: [
    "LinkedIn: https://www.linkedin.com/in/stefan-bartl",
    "XMind Roadmap: https://xmind.ai/share/k2PSPlst"
  ],
  currentlyLearning: ["Architecture", "Intermediate Go", "OS internals"]
};
````

## Achievements

[![trophy](https://github-profile-trophy.vercel.app/?username=StefanBartl\&title=-Stars,-Followers,-Reviews,-PullRequest\&theme=discord\&no-bg=false\&no-frame=true)](https://github.com/ryo-ma/github-profile-trophy)
