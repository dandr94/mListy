//https://codepen.io/mrvinrsk/pen/GRBaOGJ

if (document.querySelector(".fixed")) {
  document.querySelector(".fixed .handle").addEventListener("click", () => {
    document.querySelector(".fixed").classList.toggle("hidden");

    if (!document.querySelector(".fixed").classList.contains("hidden")) {
      if(document.querySelector(".fixed").hasAttribute("data-auto-close")) {
        let duration = document.querySelector(".fixed").dataset.autoClose || 10000;
        if(duration < 1000) duration = 1000;

        setTimeout(() => {
          document.querySelector(".fixed").classList.add("hidden");
        }, duration);
      }
    }
  });

  setTimeout(() => {
    document.querySelector(".fixed").classList.add("hidden");
    document.querySelector(".fixed").classList.remove("first");
  }, 1500);
}
