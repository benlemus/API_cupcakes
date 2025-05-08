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

// ADD CUPCAKE

$("#add_cupcake_form").on("submit", async function (e) {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);

  let data = null;

  if (formData.get("image").includes("https://")) {
    data = {
      flavor: formData.get("flavor").toLowerCase(),
      size: formData.get("size").toLowerCase(),
      rating: formData.get("rating").toLowerCase(),
      image: formData.get("image"),
    };
  } else {
    data = {
      flavor: formData.get("flavor").toLowerCase(),
      size: formData.get("size").toLowerCase(),
      rating: formData.get("rating").toLowerCase(),
      image: formData.get("https://tinyurl.com/demo-cupcake"),
    };
  }

  const res = await axios.post("/api/cupcakes", data);

  window.location.href = "/";
});

// DELETE CUPCAKE

$(document).ready(() => {
  $(document).on("click", ".delete_btn", async function (e) {
    const res = await axios.delete(`/api/cupcakes/${$(this).data("id")}`);

    window.location.href = "/";
  });
});

// UPDATE CUPCAKE

$("#update_cupcake_form").on("submit", async function (e) {
  e.preventDefault();
  const form = e.target;
  const cupcakeId = form.dataset.id;

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

  const res = await axios.patch(`/api/cupcakes/${cupcakeId}`, data);

  window.location.href = "/";
});

// CREATE CARD

function create_card(cupcake) {
  const cardContainer = document.createElement("div");
  cardContainer.style = "max-width: 30rem";
  cardContainer.className = "col-md-4 d-flex justify-content-center mt-4";

  const card = document.createElement("div");
  card.className = "card";
  card.setAttribute("data-cupcakeId", cupcake.id);

  const image = document.createElement("img");
  image.src = cupcake.image;
  image.className = "card-img-top";
  image.setAttribute("data-cupcakeId", cupcake.id);

  const cardBody = document.createElement("div");
  cardBody.className = "card-body";
  cardBody.setAttribute("data-cupcakeId", cupcake.id);

  const flavor = document.createElement("h5");
  flavor.className = "card-title";
  flavor.textContent =
    cupcake.flavor[0].toUpperCase() + cupcake.flavor.substring(1);
  flavor.setAttribute("data-cupcakeId", cupcake.id);

  const size = document.createElement("h6");
  size.className = "card-subtitle mb-2 text-body-secondary";
  size.textContent = cupcake.size;
  size.setAttribute("data-cupcakeId", cupcake.id);

  const btnContainer = document.createElement("div");

  const delete_btn = document.createElement("a");
  delete_btn.className = "btn btn-outline-danger delete_btn";
  delete_btn.textContent = "Delete";
  delete_btn.setAttribute("data-id", `${cupcake.id}`);

  const update_btn = document.createElement("a");
  update_btn.className = "btn btn-outline-success ms-2 update_btn";
  update_btn.textContent = "Update";
  update_btn.href = `/cupcakes/${cupcake.id}/update`;
  update_btn.setAttribute("data-id", `${cupcake.id}`);

  btnContainer.appendChild(delete_btn);
  btnContainer.appendChild(update_btn);

  cardContainer.appendChild(card);
  card.appendChild(image);
  card.appendChild(cardBody);
  cardBody.appendChild(flavor);
  cardBody.appendChild(size);
  for (let i = 0; i <= cupcake.rating - 1; i++) {
    if (i < 6) {
      if (i == 4 || i == 5) {
        const plusIcon = document.createElement("span");
        plusIcon.className = "material-symbols-outlined";
        plusIcon.textContent = "add";
        plusIcon.setAttribute("data-cupcakeId", cupcake.id);
        cardBody.appendChild(plusIcon);
      } else {
        const heartIcon = document.createElement("span");
        heartIcon.className = "material-symbols-outlined";
        heartIcon.textContent = "favorite";
        heartIcon.setAttribute("data-cupcakeId", cupcake.id);
        cardBody.appendChild(heartIcon);
      }
    }
  }
  cardBody.appendChild(btnContainer);

  $(".row").append(cardContainer);
}
