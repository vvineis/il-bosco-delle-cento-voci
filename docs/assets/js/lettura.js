/* Strumenti di lettura: dimensione del testo, memorizzata nel browser. */
(function () {
  "use strict";

  var CHIAVE = "bcv-dimensione-testo";
  var MISURE = [1.0, 1.15, 1.35, 1.6, 1.9]; // rem
  var PREDEFINITA = 1;

  function indiceSalvato() {
    var salvato = parseInt(window.localStorage.getItem(CHIAVE), 10);
    if (isNaN(salvato) || salvato < 0 || salvato >= MISURE.length) return PREDEFINITA;
    return salvato;
  }

  var indice = indiceSalvato();

  function applica() {
    document.documentElement.style.setProperty("--testo-racconto", MISURE[indice] + "rem");
    try { window.localStorage.setItem(CHIAVE, String(indice)); } catch (e) { /* modalità privata */ }
    var stato = document.getElementById("stato-testo");
    if (stato) stato.textContent = "Testo " + Math.round(MISURE[indice] * 100 / MISURE[PREDEFINITA]) + "%";
  }

  function cambia(delta) {
    indice = Math.min(MISURE.length - 1, Math.max(0, indice + delta));
    applica();
  }

  document.addEventListener("DOMContentLoaded", function () {
    var piu = document.getElementById("testo-piu");
    var meno = document.getElementById("testo-meno");
    if (piu) piu.addEventListener("click", function () { cambia(1); });
    if (meno) meno.addEventListener("click", function () { cambia(-1); });
    applica();
  });

  // applica subito, prima del rendering, per evitare lo sfarfallio
  applica();
})();
