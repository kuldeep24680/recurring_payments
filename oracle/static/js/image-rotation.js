$(document).ready(function(){
    var degrees = 0
    function rotateEl(event) {
      degrees += 90;
      el = event.data.param1;
      $(el).css({
        'transform': 'rotate(' + degrees + 'deg)',
        '-ms-transform': 'rotate(' + degrees + 'deg)',
        '-moz-transform': 'rotate(' + degrees + 'deg)',
        '-webkit-transform': 'rotate(' + degrees + 'deg)',
        '-o-transform': 'rotate(' + degrees + 'deg)'
      });
    }
    $('#btn-rotate-adhar-front').click({param1: '.preview-adhar-front'},rotateEl);
    $('#btn-rotate-adhar-back').click({param1: '.preview-adhar-back'},rotateEl);
    $('#btn-rotate-voterid-front').click({param1: '.preview-voterid-front'},rotateEl);
    $('#btn-rotate-voterid-back').click({param1: '.preview-voterid-back'},rotateEl);
    $('#btn-rotate-pan-card').click({param1: '#applicant_pan_card_kyc_pan_card_1_ImagePreview'},rotateEl);
    $('#btn-rotate-borrower-photo').click({param1: '#applicant_personal_docs_borrower_1_ImagePreview'},rotateEl);
    $('#btn-rotate-coborrower-photo').click({param1: '#applicant_personal_docs_coborrower_1_ImagePreview'},rotateEl);
    $('#btn-rotate-ration-card').click({param1: '#applicant_personal_docs_ration_card_1_ImagePreview'},rotateEl);
    $('#btn-rotate-bank-statement').click({param1: '#applicant_personal_docs_bank_statement_1_ImagePreview'},rotateEl);
    $('#btn-rotate-paytm-form').click({param1: '#applicant_personal_docs_paytm_form_1_ImagePreview'},rotateEl);
    $('#btn-rotate-paytm-signature').click({param1: '#applicant_personal_docs_paytm_signature_1_ImagePreview'},rotateEl);
    $('#btn-rotate-other-doc').click({param1: '#applicant_personal_docs_other_doc_1_ImagePreview'},rotateEl);
    $('#btn-rotate-other-doc').click({param1: '#applicant_personal_docs_other_doc_1_ImagePreview'},rotateEl);
    $('#btn-rotate-kyc-signature').click({param1: '#applicant_kyc_details_signature_ImagePreview'},rotateEl);
    $('#btn-rotate-kyc-adhar-front').click({param1: '.preview-kyc-adhar-front'},rotateEl);
    $('#btn-rotate-kyc-adhar-back').click({param1: '.preview-kyc-adhar-back'},rotateEl);
    $('#btn-rotate-kyc-voterid-front').click({param1: '.preview-kyc-voterid-front'},rotateEl);
    $('#btn-rotate-kyc-voterid-back').click({param1: '.preview-kyc-voterid-back'},rotateEl);
    $('#btn-rotate-kyc-pan-card').click({param1: '#guarantor1_pan_card_guarantor_pan_1_ImagePreview'},rotateEl);
    $('#btn-rotate-kyc-other-doc').click({param1: '.preview-kyc-other-doc'},rotateEl);
    $('#btn-rotate-acceptance-letter').click({param1: '.acceptance-letter-preview'},rotateEl);
    $('#btn-rotate-noc-doc').click({param1: '.noc-doc-preview'},rotateEl);
});