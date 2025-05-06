// SHOW ALL CUPCAKES
$(document).ready(getCupcakes);

async function getCupcakes() {
  const res = await axios.get("/api/cupcakes");
  const cupcakes = res.data.cupcakes;

  $(".row").empty();

  cupcakes.forEach((cupcake) => create_card(cupcake));
}

// SEARCH FORM
$("#search_form").on("keyup", () => {
  const input = $("#search_input").val();
  searchCupcakes(input);
});

async function searchCupcakes(input) {
  let cupcakes = null;
  if (input != "") {
    const res = await axios.get(`/api/cupcakes/search/${input}`);
    cupcakes = res.data;
  } else {
    const res = await axios.get("/api/cupcakes");
    cupcakes = res.data.cupcakes;
  }

  $(".row").empty();

  cupcakes.forEach((cupcake) => create_card(cupcake));
}

// ADD CUPCAKE FORM
$("#add_cupcake_form").on("submit", async function (e) {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);

  let data = null;

  if (formData.get("image").includes("https://")) {
    data = {
      flavor: formData.get("flavor"),
      size: formData.get("size"),
      rating: formData.get("rating"),
      image: formData.get("image"),
    };
  } else {
    data = {
      flavor: formData.get("flavor"),
      size: formData.get("size"),
      rating: formData.get("rating"),
      image: formData.get("https://tinyurl.com/demo-cupcake"),
    };
  }

  const res = await axios.post("/api/cupcakes", data);

  window.location.href = "/";
});

function create_card(cupcake) {
  const cardContainer = document.createElement("div");
  cardContainer.id = "cardContainer";
  cardContainer.style = "max-width: 30rem";
  cardContainer.className = "col-md-4 d-flex justify-content-center";

  const card = document.createElement("div");
  card.id = "card";
  card.className = "card";

  const image = document.createElement("img");
  image.src = cupcake.image;
  image.className = "card-img-top";

  const cardBody = document.createElement("div");
  cardBody.id = "card_body";
  cardBody.className = "card-body";

  const flavor = document.createElement("h5");
  flavor.className = "card-title";
  flavor.textContent = cupcake.flavor;

  const deleteIcon = document.createElement("span");
  deleteIcon.className = "material-symbols-outlined text-danger";
  deleteIcon.textContent = "close";
  deleteIcon.id = "delete_icon";
  deleteIcon.data;
  deleteIcon.setAttribute("data-id", `${cupcake.id}`);

  const size = document.createElement("h6");
  size.className = "card-subtitle mb-2 text-body-secondary";
  size.textContent = cupcake.size;

  cardContainer.appendChild(card);
  card.appendChild(image);
  card.appendChild(cardBody);
  cardBody.appendChild(flavor);
  flavor.appendChild(deleteIcon);
  cardBody.appendChild(size);
  for (let i = 0; i <= cupcake.rating - 1; i++) {
    if (i < 6) {
      if (i == 4 || i == 5) {
        const plusIcon = document.createElement("span");
        plusIcon.className = "material-symbols-outlined";
        plusIcon.textContent = "add";
        cardBody.appendChild(plusIcon);
      } else {
        const heartIcon = document.createElement("span");
        heartIcon.className = "material-symbols-outlined";
        heartIcon.textContent = "favorite";
        cardBody.appendChild(heartIcon);
      }
    }
  }
  $(".row").append(cardContainer);
}

// DELETE CUPCAKE

$(document).ready(() => {
  $(document).on("click", "#delete_icon", async function (e) {
    const res = await axios.delete(`/api/cupcakes/${$(this).data("id")}`);

    window.location.href = "/";
  });
});
