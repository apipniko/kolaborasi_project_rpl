// Memastikan HTML dimuat sepenuhnya sebelum menjalankan script
document.addEventListener('DOMContentLoaded', function() {
    const searchBar = document.getElementById('search-bar');
    const dropdown = document.getElementById('suggestion-dropdown');
    const suggestionList = document.getElementById('suggestion-list');

    let timeoutId;

    searchBar.addEventListener('input', function() {
        const query = this.value.trim();

        if (query.length === 0) {
            dropdown.classList.add('hidden');
            return;
        }

        clearTimeout(timeoutId);
        timeoutId = setTimeout(async () => {
            try {
                const response = await fetch(`/api/suggest?q=${encodeURIComponent(query)}`);
                const data = await response.json();

                suggestionList.innerHTML = '';

                if (data.length > 0) {
                    dropdown.classList.remove('hidden');

                    data.forEach(item => {
                        const li = document.createElement('li');
                        li.className = "px-4 py-3 hover:bg-blue-50 cursor-pointer flex justify-between items-center transition-colors";
                        
                        li.innerHTML = `
                            <div>
                                <p class="font-bold text-gray-800 text-sm">${item.product_name}</p>
                        
                            </div>
                        `;

                        li.addEventListener('click', () => {
                            searchBar.value = item.product_name;
                            dropdown.classList.add('hidden');
                        });

                        suggestionList.appendChild(li);
                    });
                } else {
                    dropdown.classList.add('hidden');
                }
            } catch (error) {
                console.error("Gagal memuat rekomendasi:", error);
            }
        }, 300); 
    });

    document.addEventListener('click', function(e) {
        if (!searchBar.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.add('hidden');
        }
    });
});