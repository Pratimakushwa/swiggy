// basic JS enhancements
console.log('Custom scripts loaded');

// sidebar cart controls
function recalcSidebarTotal() {
    let total = 0;
    document.querySelectorAll('#sidebar-cart-form .list-group-item').forEach(li => {
        const price = parseFloat(li.getAttribute('data-price')) || 0;
        const input = li.querySelector('.qty-input');
        const qty = parseInt(input.value) || 0;
        total += price * qty;
    });
    document.getElementById('sidebar-total').textContent = total.toFixed(2);
}

document.addEventListener('click', function(evt){
    if(evt.target.matches('.btn-increase') || evt.target.matches('.btn-decrease')){
        const fid = evt.target.getAttribute('data-food');
        const input = document.querySelector("input[name='qty_"+fid+"']");
        let val = parseInt(input.value) || 0;
        if(evt.target.matches('.btn-increase')) val++;
        else val = Math.max(0, val-1);
        input.value = val;
        recalcSidebarTotal();
    }
});

// recalc when quantity manually changed
document.addEventListener('input', function(evt){
    if(evt.target.matches('.qty-input')){
        recalcSidebarTotal();
    }
});

// initial calculation
document.addEventListener('DOMContentLoaded', recalcSidebarTotal);
