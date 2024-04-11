
$(document).ready(function () {
    $("#id_data_vencimento").datepicker({ dateFormat: "dd/mm/yy" });
    $("#id_data_entrada").datepicker({ dateFormat: "dd/mm/yy" });
    $("#txbDataInicio").datepicker({ dateFormat: "dd/mm/yy" });
    $("#txbDataFim").datepicker({ dateFormat: "dd/mm/yy" });
});

function validarValor() {
    var valor = parseFloat($("#id_valor").val());
    $("#id_valor").val($("#id_valor").val().replace(",", ".")); // Gambiara :(

    if(isNaN(valor)){
        alert('O conteúdo para o campo "Valor" deve ser um numero!');
        return false;
    }
}

function excluirReceita(id) {
    if(confirm("Deseja realmente excluir esse registro?") == true)
        window.location = '/excluir/receita/' + id;
}

function excluirDespesa(id) {
    if(confirm("Deseja realmente excluir esse registro?") == true)
        window.location = '/excluir/despesa/' + id;
}

