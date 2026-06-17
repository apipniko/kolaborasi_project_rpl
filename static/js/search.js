// Memastikan HTML dimuat sepenuhnya sebelum menjalankan script
document.addEventListener('DOMContentLoaded', function() {
    const searchBar = document.getElementById('search-bar');
    const dropdown = document.getElementById('suggestion-dropdown');
    const suggestionList = document.getElementById('suggestion-list');

    // Pastikan elemen ada sebelum menambahkan event listener
    if (!searchBar || !dropdown || !suggestionList) {
        console.error('Elemen search tidak ditemukan!');
        return;
    }

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
                            <div class="flex items-center gap-3">
                                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                                </svg>
                                <div>
                                    <p class="font-bold text-gray-800 text-sm">${item.product_name}</p>
                                    
                                </div>
                            </div>
                        `;

                        li.addEventListener('click', () => {
                            searchBar.value = item.product_name;
                            dropdown.classList.add('hidden');
                            
                            // Optional: Auto-submit form setelah memilih suggestion
                            // searchBar.closest('form').submit();
                        });

                        suggestionList.appendChild(li);
                    });
                } else {
                    dropdown.classList.add('hidden');
                }
            } catch (error) {
                console.error("Gagal memuat rekomendasi:", error);
                dropdown.classList.add('hidden');
            }
        }, 300); 
    });

    // Sembunyikan dropdown saat klik di luar
    document.addEventListener('click', function(e) {
        if (!searchBar.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.add('hidden');
        }
    });

    // Sembunyikan dropdown saat input tidak lagi fokus (opsional)
    searchBar.addEventListener('blur', function() {
        // Delay untuk memberi waktu klik suggestion
        setTimeout(() => {
            if (!dropdown.matches(':hover')) {
                dropdown.classList.add('hidden');
            }
        }, 200);
    });

    // Navigasi keyboard (opsional - arrow keys)
    let selectedIndex = -1;
    searchBar.addEventListener('keydown', function(e) {
        const items = suggestionList.querySelectorAll('li');
        
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
            updateSelection(items);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            selectedIndex = Math.max(selectedIndex - 1, -1);
            updateSelection(items);
        } else if (e.key === 'Enter' && selectedIndex >= 0) {
            e.preventDefault();
            items[selectedIndex].click();
        } else if (e.key === 'Escape') {
            dropdown.classList.add('hidden');
            selectedIndex = -1;
        }
    });

    function updateSelection(items) {
        items.forEach((item, index) => {
            if (index === selectedIndex) {
                item.classList.add('bg-blue-50');
            } else {
                item.classList.remove('bg-blue-50');
            }
        });
    }
});