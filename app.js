const API_URL = "https://my-fastapi-service.vercel.app";

let allSneakers = [];       // full dataset, fetched once
let activeBrand = "all";    // current filter tab


// GET ALL SNEAKERS
async function loadSneakers() {
    try {
        const response = await fetch(`${API_URL}/sneakers`);
        const data = await response.json();
        allSneakers = data.sneakers;
        buildBrandTiles(allSneakers);
        buildFilterTabs(allSneakers);
        renderSneakers(allSneakers);
    }
    catch (error) {
        console.error(error);
        document.getElementById("sneakerList").innerHTML = "Unable to connect to the API.";
    }
}


// BUILD "TOP BRANDS" STRIP
function buildBrandTiles(sneakers) {
    const brandTiles = document.getElementById("brandTiles");
    const brands = [...new Set(sneakers.map(s => s.brand))];

    brandTiles.innerHTML = "";
    brands.forEach(brand => {
        const tile = document.createElement("div");
        tile.className = "brand-tile";
        tile.textContent = brand;
        tile.onclick = () => filterByBrand(brand);
        brandTiles.appendChild(tile);
    });
}


// BUILD FILTER TABS (ALL + one per brand)
function buildFilterTabs(sneakers) {
    const filterTabs = document.getElementById("filterTabs");
    const brands = [...new Set(sneakers.map(s => s.brand))];

    filterTabs.innerHTML = `<button class="filter-tab active" data-brand="all" onclick="filterByBrand('all')">All</button>`;
    brands.forEach(brand => {
        filterTabs.innerHTML += `<button class="filter-tab" data-brand="${brand}" onclick="filterByBrand('${brand}')">${brand}</button>`;
    });
}


// FILTER BY BRAND (client-side, since we already have the full dataset)
function filterByBrand(brand) {
    activeBrand = brand;

    document.querySelectorAll(".filter-tab").forEach(tab => {
        tab.classList.toggle("active", tab.dataset.brand === brand);
    });

    const filtered = brand === "all"
        ? allSneakers
        : allSneakers.filter(s => s.brand === brand);

    renderSneakers(filtered);
}


// RENDER SNEAKER CARDS
function renderSneakers(sneakers) {
    const sneakerList = document.getElementById("sneakerList");
    const resultCount = document.getElementById("resultCount");

    sneakerList.innerHTML = "";
    resultCount.textContent = `${sneakers.length} result${sneakers.length === 1 ? "" : "s"}`;

    sneakers.forEach(sneaker => {
        const card = document.createElement("div");
        card.className = "sneaker-card";
        card.onclick = () => viewSneaker(sneaker.id);
        card.innerHTML = `
            <div class="sneaker-image"><img src="images/${sneaker.id}.jpg" alt="${sneaker.brand} ${sneaker.model}"></div>
            <div class="sneaker-info">
                <div class="sneaker-brand-row">
                    <span class="sneaker-brand">${sneaker.brand}</span>
                    <span class="sneaker-year">${sneaker.year}</span>
                </div>
                <div class="sneaker-model">${sneaker.model}</div>
                <p class="sneaker-desc">${sneaker.description}</p>
                <div class="sneaker-footer">
                    <span class="sneaker-colorway">${sneaker.colorway}</span>
                    <span class="sneaker-price">${sneaker.price}</span>
                </div>
            </div>
        `;
        sneakerList.appendChild(card);
        const img = card.querySelector("img");
        const logFit = () => {
            const box = card.querySelector(".sneaker-image");
            const cs = getComputedStyle(img);
            const nw = img.naturalWidth;
            const nh = img.naturalHeight;
            const cw = img.clientWidth;
            const ch = img.clientHeight;
            const boxW = box.clientWidth;
            const boxH = box.clientHeight;
            const coverScale = Math.max(boxW / nw, boxH / nh);
            const containScale = Math.min(boxW / nw, boxH / nh);
            // #region agent log
            fetch('http://127.0.0.1:7348/ingest/8de4df9d-4133-4776-bff2-6662d3aec6af',{method:'POST',headers:{'Content-Type':'application/json','X-Debug-Session-Id':'491361'},body:JSON.stringify({sessionId:'491361',runId:'pre-fix',hypothesisId:sneaker.id===10||sneaker.id===19?'A':'D',location:'app.js:renderSneakers',message:'img fit',data:{id:sneaker.id,model:sneaker.model,nw,nh,cw,ch,boxW,boxH,objectFit:cs.objectFit,coverScale,containScale,cropped:coverScale>containScale},timestamp:Date.now()})}).catch(()=>{});
            // #endregion
        };
        if (img.complete && img.naturalWidth) logFit();
        else img.addEventListener("load", logFit, { once: true });
    });
}


// GET ONE SNEAKER
async function viewSneaker(id) {
    try {
        const response = await fetch(`${API_URL}/sneakers/${id}`);
        const sneaker = await response.json();

        alert(`
            ${sneaker.year} ${sneaker.brand} ${sneaker.model}
            Colorway:
            ${sneaker.colorway}

            Price:
            ${sneaker.price}

            Description:
            ${sneaker.description}
        `);
    }
    catch (error) {
        console.error(error);
        alert("Unable to retrieve sneaker.");
    }
}


// SEARCH (uses the live API's search endpoint)
async function searchSneakers() {
    const query = document.getElementById("searchInput").value;
    if (!query) {
        clearSearch();
        return;
    }
    try {
        const response = await fetch(`${API_URL}/sneakers/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        activeBrand = "all";
        document.querySelectorAll(".filter-tab").forEach(tab => {
            tab.classList.toggle("active", tab.dataset.brand === "all");
        });
        renderSneakers(data.results);
    }
    catch (error) {
        console.error(error);
        alert("Search failed.");
    }
}


// SHOW ALL / CLEAR SEARCH
function clearSearch() {
    document.getElementById("searchInput").value = "";
    activeBrand = "all";
    document.querySelectorAll(".filter-tab").forEach(tab => {
        tab.classList.toggle("active", tab.dataset.brand === "all");
    });
    renderSneakers(allSneakers);
}


loadSneakers();
