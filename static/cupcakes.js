$(document).ready(get_cupcakes);

async function get_cupcakes() {
  const resp = await axios.get("/api/cupcakes");
  console.log(resp);
  const cupcakes = resp.data.cupcakes;

  $("#cupcakes_list").empty();

  cupcakes.forEach((cupcake) => {
    const li = document.createElement("li");
    li.textContent = cupcake.flavor;
    $("#cupcakes_list").append(li);
  });
}

// TODO: add form
