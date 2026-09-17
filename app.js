"use strict";

const API_URL = document.body.dataset.apiUrl;

const state = {
    sneakers: [],
};

const elements = {
    brandTiles: document.getElementById("brandTiles"),
    filterTabs: document.getElementById("filterTabs"),
    resultCount: document.getElementById("resultCount"),
    searchForm: document.getElementById("searchForm"),
    searchInput: document.getElementById("searchInput"),
    showAllButton: document.getElementById("showAllButton"),
    sneakerList: document.getElementById("sneakerList"),
};


async function fetchJson(path) {
    const response = await fetch(`${API_URL}${path}`, {
        headers: { Accept: "application/json" },
    });

    if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
    }

    return response.json();
}


function uniqueBrands(sneakers) {
    return [...new Set(sneakers.map(({ brand }) => brand))];
}


function setCollectionMessage(message, isError = false, isBusy = false) {
    elements.sneakerList.replaceChildren();
    elements.sneakerList.setAttribute("aria-busy", String(isBusy));
    const status = document.createElement("p");
    status.className = isError ? "collection-status collection-status--error" : "collection-status";
    status.textContent = message;
    elements.sneakerList.appendChild(status);
}


function setActiveBrand(brand) {
    document.querySelectorAll(".filter-tab").forEach((tab) => {
        const isActive = tab.dataset.brand === brand;
        tab.classList.toggle("active", isActive);
        tab.setAttribute("aria-pressed", String(isActive));
    });
}


function createBrandButton(brand) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "brand-tile";
    button.textContent = brand;
    button.addEventListener("click", () => filterByBrand(brand));
    return button;
}


function createFilterButton(brand) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "filter-tab";
    button.dataset.brand = brand;
    button.textContent = brand === "all" ? "All" : brand;
    button.setAttribute("aria-pressed", String(brand === "all"));
    button.addEventListener("click", () => filterByBrand(brand));
    return button;
}


function buildNavigation(sneakers) {
    const brands = uniqueBrands(sneakers);
    elements.brandTiles.replaceChildren(...brands.map(createBrandButton));
    elements.filterTabs.replaceChildren(
        createFilterButton("all"),
        ...brands.map(createFilterButton),
    );
}


function getImageClass(sneakerId) {
    if (sneakerId === 10) return "sneaker-image sneaker-image--jordan4";
    if (sneakerId === 19) return "sneaker-image sneaker-image--shockwave";
    return "sneaker-image";
}


function createTextElement(tagName, className, text) {
    const element = document.createElement(tagName);
    element.className = className;
    element.textContent = text;
    return element;
}


function createSneakerCard(sneaker, index) {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "sneaker-card";
    card.setAttribute("aria-label", `View ${sneaker.brand} ${sneaker.model}`);
    card.addEventListener("click", () => viewSneaker(sneaker.id));

    const imageWrapper = document.createElement("span");
    imageWrapper.className = getImageClass(sneaker.id);

    const image = document.createElement("img");
    image.src = `images/${sneaker.id}.jpg`;
    image.alt = `${sneaker.brand} ${sneaker.model}`;
    image.loading = index < 4 ? "eager" : "lazy";
    image.decoding = "async";
    imageWrapper.appendChild(image);

    const info = document.createElement("span");
    info.className = "sneaker-info";

    const brandRow = document.createElement("span");
    brandRow.className = "sneaker-brand-row";
    brandRow.append(
        createTextElement("span", "sneaker-brand", sneaker.brand),
        createTextElement("span", "sneaker-year", sneaker.year),
    );

    const footer = document.createElement("span");
    footer.className = "sneaker-footer";
    footer.append(
        createTextElement("span", "sneaker-colorway", sneaker.colorway),
        createTextElement("span", "sneaker-price", sneaker.price),
    );

    info.append(
        brandRow,
        createTextElement("span", "sneaker-model", sneaker.model),
        createTextElement("span", "sneaker-desc", sneaker.description),
        footer,
    );
    card.append(imageWrapper, info);

    return card;
}


function renderSneakers(sneakers) {
    elements.sneakerList.setAttribute("aria-busy", "false");
    elements.resultCount.textContent = `${sneakers.length} result${sneakers.length === 1 ? "" : "s"}`;

    if (sneakers.length === 0) {
        setCollectionMessage("No sneakers matched your search.");
        return;
    }

    const cards = sneakers.map(createSneakerCard);
    elements.sneakerList.replaceChildren(...cards);
}


function filterByBrand(brand) {
    setActiveBrand(brand);
    const filtered = brand === "all"
        ? state.sneakers
        : state.sneakers.filter((sneaker) => sneaker.brand === brand);
    renderSneakers(filtered);
}


async function viewSneaker(id) {
    try {
        const sneaker = await fetchJson(`/sneakers/${id}`);
        alert(`${sneaker.year} ${sneaker.brand} ${sneaker.model}\n\nColorway: ${sneaker.colorway}\nPrice: ${sneaker.price}\n\n${sneaker.description}`);
    } catch (error) {
        console.error("Unable to retrieve sneaker:", error);
        alert("Unable to retrieve this sneaker right now.");
    }
}


async function searchSneakers(query) {
    setCollectionMessage("Searching sneakers…", false, true);

    try {
        const data = await fetchJson(`/sneakers/search?q=${encodeURIComponent(query)}`);
        setActiveBrand("all");
        renderSneakers(data.results);
    } catch (error) {
        console.error("Search failed:", error);
        elements.resultCount.textContent = "Search unavailable";
        setCollectionMessage("Search is unavailable right now. Please try again.", true);
    }
}


function clearSearch() {
    elements.searchInput.value = "";
    setActiveBrand("all");
    renderSneakers(state.sneakers);
}


async function loadSneakers() {
    try {
        const data = await fetchJson("/sneakers");
        state.sneakers = data.sneakers;
        buildNavigation(state.sneakers);
        renderSneakers(state.sneakers);
    } catch (error) {
        console.error("Unable to load sneakers:", error);
        elements.resultCount.textContent = "Unavailable";
        setCollectionMessage("Unable to connect to the sneaker catalog.", true);
    }
}


elements.searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const query = elements.searchInput.value.trim();
    if (query) searchSneakers(query);
    else clearSearch();
});

elements.showAllButton.addEventListener("click", clearSearch);
loadSneakers();
