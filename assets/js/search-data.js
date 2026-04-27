// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-blog",
          title: "blog",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/blog/";
          },
        },{id: "nav-projects",
          title: "projects",
          description: "Some of the projects I have done! (Under construction)",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "post-einstein-notation",
        
          title: "Einstein notation",
        
        description: "Wrapping up vector calculus computations",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2019/einstein-notation/";
          
        },
      },{id: "projects-pyddg",
          title: 'Pyddg',
          description: "A projective geometry library.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/PyDDG/";
            },},{id: "projects-gummy",
          title: 'gummy',
          description: "A Heuristic solver for QUBO Problems.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/gummy/";
            },},{id: "projects-physics-sim",
          title: 'Physics SIM',
          description: "A Molecular Dynamics simulator for computational experiment and physics visualization.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/physics_sim/";
            },},{id: "projects-quantum-gabidulin-codes",
          title: 'quantum Gabidulin codes',
          description: "A literature review of quantum Gabidulin code.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/quantumgabidulin/";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%61%72%79%61.%70%72%61%73%65%74%79%61%31%39%39%37@%67%6D%61%69%6C.%63%6F%6D", "_blank");
        },
      },{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/metersquared", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/prasetyaarya", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
